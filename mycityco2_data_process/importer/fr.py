import csv
import datetime
import fnmatch
import time

import pandas
import psycopg2
import requests
import xmltodict
from bs4 import BeautifulSoup
from loguru import logger

from mycityco2_data_process import const

from .base import AbstractImporter, depends

NOMENCLATURE_PARAMS: dict = {
    "M14": "M14/M14_COM_SUP3500",
    "M14A": "M14/M14_COM_INF500",
    "M57": "M57/M57",
}
NOMENCLATURE: list = list(NOMENCLATURE_PARAMS.keys())

CHART_OF_ACCOUNT_URL: str = (
    "http://odm-budgetaire.org/composants/normes/2021/{}/planDeCompte.xml"
)

FR_PATH_FILE = const.settings.PATH / "data" / "fr"

COA_CONDITION_FILE = FR_PATH_FILE / "coa_condition.csv"
COA_CATEGORIES_FILE = FR_PATH_FILE / "coa_categories.csv"


def _get_chart_account(dictionnary: dict, result_list: list = []):
    value_list = dictionnary.get("Compte")

    if value_list:
        result_dict = {}
        for i in value_list:
            if isinstance(i, dict):
                result = {"name": i.get("@Libelle")}
                result_list.append(result | {"code": i.get("@Code")})

                _get_chart_account(i, result_list)
            else:
                result_dict |= {i: value_list[i]}
        if len(result_dict) > 0:
            result = {"name": result_dict.get("@Libelle")}
            result_list.append(result | {"code": result_dict.get("@Code")})

    result_list.sort(key=lambda x: x["code"])

    return result_list


class FrImporter(AbstractImporter):
    def __init__(
        self,
        limit: int = 50,
        offset: int = 0,
        departement: int = 74,
        env=None,
        db=const.settings.ENV_DB,
        dataset: list = [],
    ):
        super().__init__(env=env, db=db)
        self.rename_fields: dict = {"com_name": "name", "com_siren_code": "district"}
        self._dataset = dataset
        self._city_amount: int = 0

        self.url: str = f"https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-france-commune&q=&sort=com_name&rows={limit}&start={offset}&refine.dep_code={departement}"

    @property
    def source_name(self):
        return "API"

    @property
    def currency_name(self):
        return "EUR"

    @depends("rename_fields")
    def get_cities(self):
        data = self._dataset

        if not len(data):
            data = requests.get(self.url).json().get("records")

        final_data = []

        for city in data:
            city = city.get("fields")

            final_data.append({v: city.get(k) for k, v in self.rename_fields.items()})

        self._city_amount += len(final_data)

        return final_data

    @depends("city_ids")
    def get_journal_data(self):
        journals_ids = []

        for city in self.city_ids:
            journals_ids.append(
                {
                    "type": "general",
                    "code": "IMMO",
                    "company_id": city.id,
                    "name": "Immobilisations",
                }
            )
            journals_ids.append(
                {
                    "type": "general",
                    "code": "BUD",
                    "company_id": city.id,
                    "name": "Journal",
                }
            )

        return journals_ids

    def gen_account_account_data(self):
        self.step2_1 = 0
        step2_1_start_timer = time.perf_counter()
        nomens = NOMENCLATURE
        logger.debug(f"{self._db} - Generating {', '.join(nomens)} account set")

        final_accounts = {}

        for nomen in nomens:
            logger.debug(f"{self._db} - Generating {nomen} account set")
            nomen_param = NOMENCLATURE_PARAMS.get(nomen)
            if not nomen_param:
                raise AttributeError(
                    f"FR - No configuration found for nomenclature: {nomen}"
                )

            res = requests.get(CHART_OF_ACCOUNT_URL.format(nomen_param))
            content = res.content
            data = xmltodict.parse(BeautifulSoup(content, "xml").prettify())
            account = data.get("Nomenclature").get("Nature").get("Comptes")
            accounts = _get_chart_account(account, [])

            if not any(dictionnary["code"] == "65888" for dictionnary in accounts):
                accounts.append(
                    {
                        "name": "Autres",
                        "code": "65888",
                    }
                )

            final_accounts[nomen] = accounts

        step2_1_end_timer = time.perf_counter()
        self.step2_1 += step2_1_end_timer - step2_1_start_timer

        self.account_account_ids = final_accounts
        logger.debug(
            f"{self._db} - All {', '.join(nomens)} account set has been generated"
        )
        return final_accounts

    # TODO: Do list comprehension
    def gen_carbon_factors(self):
        if not self.carbon_factor:
            categories = []
            with open(const.settings.CARBON_FILE, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    categories.append(
                        {
                            "condition": row.get("condition"),
                            "id": self.env.ref(row.get("external id carbon.factor")),
                            "rule_order": row.get("rule_order", 0),
                        }
                    )

            self.carbon_factor = sorted(categories, key=lambda x: x["rule_order"])

        return self.carbon_factor

    @depends("city_ids")
    def get_account_account_data(self):
        logger.debug(f"{self._db} - Generating account")
        accounts = self.gen_account_account_data()

        self.step2_2 = 0
        step2_2_start_timer = time.perf_counter()

        url = "https://data.economie.gouv.fr/api/v2/catalog/datasets/balances-comptables-des-communes-en-{}/exports/json?offset=0&refine={}&refine=siren%3A{}&limit=1&timezone=UTC"

        account_account_ids = []

        for city in self.city_ids:
            logger.debug(f"{self._db} - Generating account set for {city.name}")

            # Hardcoded year because the API change filter type on 2015
            refine_parameter = (
                "budget:BP" if const.settings.YEAR[-1] <= 2015 else "cbudg:1"
            )

            res_nomen = requests.get(
                url.format(
                    const.settings.YEAR[-1], refine_parameter, city.company_registry
                )
            )

            nomen = res_nomen.json()[0].get("nomen")

            account_account_ids.append(
                {
                    "code": "000",
                    "name": "Placeholder",
                    "company_id": city.id,
                    "account_type": const.settings.DEFAULT_ACCOUNT_TYPE,
                }
            )

            for account in accounts.get(nomen):
                name = account.get("name")
                code = account.get("code")

                account_id = {
                    "code": code,
                    "name": name,
                    "company_id": city.id,
                    "account_type": const.settings.DEFAULT_ACCOUNT_TYPE,
                }

                for account in self.gen_carbon_factors():
                    if fnmatch.fnmatch(code, account.get("condition")):
                        account_id |= {
                            "use_carbon_value": True,
                            "carbon_in_is_manual": True,
                            "carbon_in_factor_id": account.get("id").id,
                            "carbon_in_compute_method": "monetary",
                            "carbon_out_compute_method": "monetary",
                        }

                        break

                account_account_ids.append(account_id)

        step2_2_end_timer = time.perf_counter()
        self.step2_2 = step2_2_end_timer - step2_2_start_timer

        return account_account_ids

    @depends("city_ids", "journals_ids", "city_account_account_ids", "currency_id")
    def get_account_move_data(self):
        self.step3_1 = self.step3_2 = self.step3_3 = 0

        account_journal_dict = {
            record.company_id[0]: record
            for record in self.journals_ids.filtered(
                lambda record: record.code == "BUD"
            )
        }

        for city in self.city_ids:
            journal_bud = account_journal_dict[city.id]

            account_account_ids = self.city_account_account_ids.filtered(
                lambda element: element.company_id[0] == city.id
            )

            account_dict = {}
            for account in account_account_ids:
                account_dict[account.code] = account.id

            default_plan_identifier = account_dict["000"]

            for year in const.settings.YEAR:
                city_account_move_line_ids = []
                date = f"{year}-12-31"  # YEAR / MONTH / DAY

                logger.debug(
                    f"{self._db} - Generating account move set for {city.name} for {year}"
                )

                account_move_bud_id = self.create_account_move(
                    [
                        {
                            "date": date,
                            "journal_id": journal_bud.id,
                            "company_id": city.id,
                            "ref": journal_bud.name,
                        }
                    ]
                )

                # Hardcoded year because the API change filter type on 2015
                refine_parameter = "budget:BP" if year <= 2015 else "cbudg:1"

                step3_1_start_timer = time.perf_counter()
                url = "https://data.economie.gouv.fr/api/v2/catalog/datasets/balances-comptables-des-communes-en-{}/exports/json?offset=0&refine=siren%3A{}&refine={}&timezone=UTC"
                step3_1_end_timer = time.perf_counter()
                self.step3_1 += step3_1_end_timer - step3_1_start_timer

                data = requests.get(
                    url.format(year, city.company_registry, refine_parameter)
                ).json()

                if isinstance(data, dict) and (
                    data.get("error_code") or data.get("status_code")
                ):
                    continue

                step3_2_start_timer = time.perf_counter()
                for i in data:

                    plan_identifier = account_dict.get(
                        i.get("compte"), default_plan_identifier
                    )

                    debit_bud = i.get("obnetdeb") + i.get("onbdeb")
                    credit_bud = i.get("obnetcre") + i.get("onbcre")

                    line_id_bud = {
                        "company_id": city.id,
                        "date": date,
                        "account_id": plan_identifier,
                        "currency_id": self.currency_id.id,
                        "move_id": account_move_bud_id.id,
                        "name": i.get("compte"),
                        # 'code-compte': plan_id.code
                    }

                    if credit_bud:
                        city_account_move_line_ids.append(
                            line_id_bud | {"debit": 0.0, "credit": credit_bud}
                        )

                    if debit_bud:
                        city_account_move_line_ids.append(
                            line_id_bud | {"debit": debit_bud, "credit": 0.0}
                        )

                step3_2_end_timer = time.perf_counter()
                self.step3_2 += step3_2_end_timer - step3_2_start_timer

                step3_3_start_timer = time.perf_counter()
                logger.debug(f"{self._db} - Sending data for {city.name} for {year}")
                account_move_lines_ids = self.env["account.move.line"].create(
                    city_account_move_line_ids
                )

                if account_move_lines_ids:
                    account_move_lines_ids.read(
                        fields=[k for k, _ in city_account_move_line_ids[0].items()]
                    )

                step3_3_end_timer = time.perf_counter()
                self.step3_3 += step3_3_end_timer - step3_3_start_timer

                self.account_move_line_ids |= account_move_lines_ids

        return self.account_move_line_ids

    def account_asset_create_categories(self):
        self.step4_1 = self.step4_2 = 0

        if not const.settings.ACCOUNT_ASSET_TOGGLE:
            return self.account_asset_categories

        account_asset_categories = {}

        account_journal_dict = {
            journal.company_id[0]: journal
            for journal in self.journals_ids.filtered(
                lambda record: record.code == "IMMO"
            )
        }

        account_account_dict = {}
        for account in self.city_account_account_ids:
            key = f"{account.company_id[0]}-{account.code}"
            account_account_dict[key] = account

        with open(const.settings.ACCOUNT_ASSET_FILE, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                carbon_id = (
                    self.env.ref(row.get("FE"))
                    if row.get("FE", "#N/A") != "#N/A"
                    else None
                )
                for city in self.city_ids:
                    step4_1_start_timer = time.perf_counter()

                    if account_account_id := account_account_dict.get(
                        f"{city.id}-{row['Code']}"
                    ):
                        vals = {
                            "name": account_account_id.name,
                            "code": "6811." + row.get("Code"),
                            "account_type": account_account_id.account_type,
                            "company_id": city.id,
                        }

                        vals |= (
                            {
                                "use_carbon_value": True,
                                "carbon_in_is_manual": True,
                                "carbon_in_factor_id": carbon_id.id,
                            }
                            if carbon_id
                            else {}
                        )

                        account_account_depreciation_id = self.env[
                            "account.account"
                        ].create(vals)

                        journal_id = account_journal_dict[city.id]

                        step4_1_end_timer = time.perf_counter()

                        self.step4_1 += step4_1_end_timer - step4_1_start_timer
                        step4_2_start_timer = time.perf_counter()

                        cat = self.env["account.asset.profile"].create(
                            {
                                "company_id": city.id,
                                "name": account_account_id.name,
                                "method_number": row["Years"],
                                "account_asset_id": account_account_id.id,
                                "account_depreciation_id": account_account_id.id,
                                "account_expense_depreciation_id": account_account_depreciation_id.id,
                                "journal_id": journal_id.id,
                            }
                        )
                        step4_2_end_timer = time.perf_counter()
                        self.step4_2 += step4_2_end_timer - step4_2_start_timer

                        account_asset_categories[account_account_id.id] = cat.id

        self.account_asset_categories = account_asset_categories

        return self.account_asset_categories

    def populate_account_asset(self):
        self.step4_3 = self.step4_4 = self.step4_5 = 0
        if not const.settings.ACCOUNT_ASSET_TOGGLE:
            return self.account_asset

        step4_3_start_timer = time.perf_counter()

        account_asset_ids = []

        for lines in self.account_move_line_ids:
            if (
                lines.name.startswith("20")
                or lines.name.startswith("21")
                and lines.debit > 0
            ):
                year = datetime.datetime.strptime(lines.date, "%Y-%m-%d").strftime("%Y")
                profile_id = self.account_asset_categories.get(lines.account_id[0])
                account_asset = {
                    "name": lines.name + "." + year,
                    "purchase_value": lines.debit,
                    "date_start": str(int(year)) + "-01-01",
                    "company_id": lines.company_id[0],
                    "profile_id": profile_id,
                }
                if profile_id:
                    account_asset_ids.append(account_asset)

        step4_3_end_timer = time.perf_counter()

        self.step4_3 += step4_3_end_timer - step4_3_start_timer

        if account_asset_ids:
            step4_4_start_timer = time.perf_counter()

            ids = self.env["account.asset"].create(account_asset_ids)
            ids.read(fields=[k for k, v in account_asset_ids[0].items()])

            step4_4_end_timer = time.perf_counter()
            self.step4_4 += step4_4_end_timer - step4_4_start_timer
            step4_5_start_timer = time.perf_counter()

            self.env["account.asset"].browse(ids.ids).validate()

            step4_5_end_timer = time.perf_counter()
            self.step4_5 += step4_5_end_timer - step4_5_start_timer

        self.account_asset = account_asset_ids

        return self.account_asset

    def account_asset_create_move(self):
        self.step4_6 = 0
        if not const.settings.ACCOUNT_ASSET_TOGGLE:
            return False

        step4_6_start_timer = time.perf_counter()

        account_asset_line_ids = self.env["account.asset.line"].search(
            [
                ("line_days", "!=", 0),
                ("init_entry", "=", False),
                ("type", "=", "depreciate"),
            ]
        )

        chunk_number = (
            len(account_asset_line_ids) // const.settings.ACCOUNT_ASSET_CHUNK_SIZE
        ) + 1
        for i in range(chunk_number):
            logger.debug(
                f"{self._db} - Account Asset Create Move {i + 1}/{chunk_number}"
            )
            account_ids = account_asset_line_ids[
                const.settings.ACCOUNT_ASSET_CHUNK_SIZE
                * i : const.settings.ACCOUNT_ASSET_CHUNK_SIZE
                * (i + 1)
            ]
            self.env["account.asset.line"].browse(account_ids.ids).create_move()

        step4_6_end_timer = time.perf_counter()

        self.step4_6 += step4_6_end_timer - step4_6_start_timer

        return True

    def export_data(self):
        co2_categories = []
        with open(COA_CATEGORIES_FILE.as_posix()) as f:
            co2_categories = list(sorted(csv.DictReader(f), key=lambda k: k["id"]))

        coa_condition = []
        with open(COA_CONDITION_FILE.as_posix()) as f:
            coa_condition = list(
                sorted(csv.DictReader(f), key=lambda k: k["rule_order"])
            )

        postegres = (
            psycopg2.connect(
                database=self._db,
                port=const.settings.SQL_PORT,
                host="localhost",
                password="odoo",
                user="odoo",
            )
            if const.settings.SQL_LOCAL
            else psycopg2.connect(
                database=self._db,
                port=const.settings.SQL_PORT,
                host="/tmp",
                user="odoo",
            )
        )

        query = """
        SELECT
        partner.company_registry AS city_id,
        company.name AS city_name,
        account.code AS account_code,
        account.name AS account_name,
        account.code||'-'||account.name AS account,
        CASE WHEN journal.code = 'IMMO' THEN 'INV' ELSE 'FCT' END AS journal_code,
        CASE WHEN journal.name = 'Immobilisations' THEN 'Investissement' ELSE 'Fonctionnement' END AS journal_name,
        EXTRACT ('Year' FROM lines.date) AS entry_year,
        lines.amount_currency AS entry_amount,
        currency.name AS entry_currency,
        lines.carbon_balance as entry_carbon_kgCO2e

        FROM res_company AS company

        INNER JOIN res_partner AS partner ON company.partner_id = partner.id
        INNER JOIN res_currency AS currency ON company.currency_id = currency.id
        INNER JOIN account_account AS account ON account.company_id = company.id
        INNER JOIN account_move_line AS lines on account.id = lines.account_id
        INNER JOIN account_journal AS journal ON lines.journal_id = journal.id and lines.company_id = journal.company_id

        WHERE EXTRACT ('Year' FROM lines.date) > 2015;
        """

        with postegres as connection:
            logger.debug(f"{self._db} - Extracting data from ODOO, using SQL")
            dataframe = pandas.read_sql_query(query, connection)

            # Habitant
            logger.debug(f"{self._db} - Matching habitant/postal code to city")
            try:
                siren_to_habitant = pandas.read_csv(
                    f"{FR_PATH_FILE.as_posix()}/siren.csv"
                )
                siren_to_postal = pandas.read_csv(
                    f"{FR_PATH_FILE.as_posix()}/postal.csv"
                ).drop_duplicates()
            except FileNotFoundError as e:
                logger.error(str(e))
                raise e

            siren_to_postal = siren_to_postal.groupby(["insee"]).agg(lambda x: list(x))

            city_data = pandas.merge(
                siren_to_habitant,
                siren_to_postal,
                how="inner",
                on="insee",
            )

            dataframe["city_id"] = dataframe["city_id"].astype(int)

            dataframe = pandas.merge(
                dataframe, city_data, how="left", left_on="city_id", right_on="siren"
            )

            # Category
            logger.debug(f"{self._db} - Matching Category to account.account")

            def matching(code):
                for row in coa_condition:
                    if fnmatch.fnmatch(code, row["condition"]):
                        return row["category_id"]
                return 0

            dataframe["category_id"] = dataframe["account_code"].apply(matching)

            dataframe = dataframe[dataframe["category_id"] != 0]

            def find_categories(categ_id):
                for row in co2_categories:
                    if row.get("id") == categ_id:
                        return (row.get("code"), row.get("name"))
                return (False, False)

            def unpack_code(vals):
                return vals[0]

            def unpack_name(vals):
                return vals[1]

            dataframe["category_tuple"] = dataframe["category_id"].apply(
                find_categories
            )

            dataframe["category_code"] = dataframe["category_tuple"].apply(unpack_code)
            dataframe["category_name"] = dataframe["category_tuple"].apply(unpack_name)

            dataframe = dataframe.drop(
                columns=[
                    "category_id",
                    "category_tuple",
                    "Reg_com",
                    "dep_com",
                    "siren",
                    "insee",
                    "nom_com",
                    "ptot_2023",
                    "pcap_2023",
                ]
            )
            dataframe = dataframe.rename(columns={"pmun_2023": "habitant"})

            dataframe = dataframe[dataframe["category_name"] != False]
            # Category

            logger.debug(f"{self._db} - Sorting dataframe")
            dataframe = dataframe.sort_values(
                by=["city_id", "account_code", "entry_year"]
            )

            logger.debug(
                f"{self._db} - Exporting dataframe to '{const.settings.PATH.as_posix()}/data/temp_file/{self._db}.csv'"
            )
            dataframe.to_csv(
                f"{const.settings.PATH.as_posix()}/data/temp_file/{self._db}.csv",
                index=False,
            )
