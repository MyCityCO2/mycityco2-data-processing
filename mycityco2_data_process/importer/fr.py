import csv
import datetime
import fnmatch
import json

import requests
import xmltodict
from bs4 import BeautifulSoup
from loguru import logger

from mycityco2_data_process import const

from .base import AbstractImporter


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


NOMENCLATURE: tuple = ("M14", "M14A", "M57")
NOMENCLATURE_PARAMS: dict = {
    "M14": "M14/M14_COM_SUP3500",
    "M14A": "M14/M14_COM_INF500",
    "M57": "M57/M57",
}

CHART_OF_ACCOUNT_URL: str = (
    "http://odm-budgetaire.org/composants/normes/2021/{}/planDeCompte.xml"
)


class FrImporter(AbstractImporter):
    def __init__(
        self,
        limit: int = 50,
        offset: int = 0,
        departement: int = 74,
        env=None,
        city_name=[],
        db=const.settings.ENV_DB,
        dataset: list = [],
    ):
        super().__init__(env)
        self._db = db
        self._wanted_city = city_name
        self.rename_fields: dict = {"com_name": "name", "com_siren_code": "district"}
        self._dataset = dataset
        self._city_amount: int = 0

        if len(self._wanted_city):
            limit = -1
            offset = 0
        self.url: str = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-france-commune&q=&sort=com_name&rows={}&start={}&refine.dep_code={}".format(
            limit, offset, departement
        )

    @property
    def source_name(self):
        return "API"

    @property
    def currency_name(self):
        return "EUR"

    @AbstractImporter.depends("rename_fields")
    def get_cities(self):
        data = self._dataset

        if not len(data):
            data = requests.get(self.url).json().get("records")

        final_data = []

        for city in data:
            city = city.get("fields")

            final_city = {}

            if len(self._wanted_city) and city.get("com_name") not in self._wanted_city:
                continue

            if city.get("com_name") in const.settings.SKIPPED_CITY:
                continue

            self._city_amount += 1
            for k in city.keys():
                if k in self.rename_fields.keys():
                    if self.rename_fields.get(k):
                        final_city[self.rename_fields.get(k)] = city[k]
                    else:
                        final_city[k] = city[k]

            final_data.append(final_city)

        return final_data

    @AbstractImporter.depends("city_ids")
    def get_journal_data(self):
        journals_ids = []

        for city in self.city_ids:
            city_id = city.id

            journal_account_asset = {
                "type": "general",
                "code": "IMMO",
                "company_id": city_id,
                "name": "Immobilisations",
            }
            journals_ids.append(journal_account_asset)

            journal_bud = {
                "type": "general",
                "code": "BUD",
                "company_id": city_id,
                "name": "Journal",
            }
            journals_ids.append(journal_bud)

        return journals_ids

    def gen_account_account_data(self):
        nomens = NOMENCLATURE
        logger.debug(f"Generating {', '.join(nomens)} account set")

        final_accounts = {}

        for nomen in nomens:
            logger.debug(f"Generating {nomen} account set")
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

            if (
                len(list(filter(lambda element: element["code"] == "65888", accounts)))
                == 0
            ):
                accounts.append(
                    {
                        "name": "Autres",
                        "code": "65888",
                    }
                )
            final_accounts[nomen] = accounts

        self.account_account_ids = final_accounts
        logger.debug(f"All {', '.join(nomens)} account set has been generated")
        return final_accounts

    def gen_carbon_factor(self):
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

    @AbstractImporter.depends("city_ids")
    def get_account_account_data(self):
        logger.debug("Generating account")
        accounts = self.gen_account_account_data()

        cities = self.city_ids

        url = "https://data.economie.gouv.fr/api/v2/catalog/datasets/balances-comptables-des-communes-en-{}/exports/json?offset=0&refine={}&refine=siren%3A{}&limit=1&timezone=UTC"

        account_account_ids = []

        for city in cities:
            logger.debug(f"Generating account set for {city.name}")
            city_id = city.id
            city_registry = city.company_registry

            refine_parameter = "cbudg:1"
            if const.settings.YEAR[-1] <= 2015:
                refine_parameter = "budget:BP"

            res_nomen = requests.get(
                url.format(const.settings.YEAR[-1], refine_parameter, city_registry)
            )

            content_nomen = res_nomen.content.decode("utf8")

            data_nomen = json.loads(content_nomen)

            nomen = data_nomen[0].get("nomen")

            account_account_ids.append(
                {
                    "code": "000",
                    "name": "Placeholder",
                    "company_id": city_id,
                    "account_type": const.settings.DEFAULT_ACCOUNT_TYPE,
                }
            )

            for account in accounts.get(nomen):
                name = account.get("name")
                code = account.get("code")

                account_id = {
                    "code": code,
                    "name": name,
                    "company_id": city_id,
                    "account_type": const.settings.DEFAULT_ACCOUNT_TYPE,
                }

                for account in self.gen_carbon_factor():
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

        return account_account_ids

    @AbstractImporter.depends(
        "city_ids", "journals_ids", "city_account_account_ids", "currency_id"
    )
    def get_account_move_data(self):
        account_journal_dict = {}
        for journal in self.journals_ids:
            if journal.code != "BUD":
                continue
            account_journal_dict[journal.company_id[0]] = journal

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
                date = "{0}-12-31".format(year)

                logger.debug(f"Generating account move set for {city.name} for {year}")

                account_move_bud_id = self.create_account_move(
                    {
                        "date": date,
                        "journal_id": journal_bud.id,
                        "company_id": city.id,
                        "ref": journal_bud.name,
                    }
                )

                if not self.account_move_ids:
                    self.account_move_ids = account_move_bud_id
                else:
                    self.account_move_ids |= account_move_bud_id

                refine_parameter = "cbudg:1"
                if year <= 2015:
                    refine_parameter = "budget:BP"

                url = "https://data.economie.gouv.fr/api/v2/catalog/datasets/balances-comptables-des-communes-en-{}/exports/json?offset=0&refine=siren%3A{}&refine={}&timezone=UTC"

                data = requests.get(
                    url.format(year, city.company_registry, refine_parameter)
                ).json()

                if isinstance(data, dict) and (
                    data.get("error_code") or data.get("status_code")
                ):
                    continue

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

                    if credit_bud != 0.0:
                        city_account_move_line_ids.append(
                            line_id_bud | {"debit": 0.0, "credit": credit_bud}
                        )

                    if debit_bud != 0.0:
                        city_account_move_line_ids.append(
                            line_id_bud | {"debit": debit_bud, "credit": 0.0}
                        )

                logger.debug(f"Sending data for {city.name} for {year}")
                account_move_lines_ids = self.env["account.move.line"].create(
                    city_account_move_line_ids
                )

                account_move_lines_ids.read(
                    fields=[k for k, v in city_account_move_line_ids[0].items()]
                ) if len(city_account_move_line_ids) else None

                if not self.account_move_line_ids:
                    self.account_move_line_ids = account_move_lines_ids
                else:
                    for account_move_line in account_move_lines_ids:
                        self.account_move_line_ids |= account_move_line

        return self.account_move_line_ids

    def account_asset_create_categories(self):
        if not const.settings.ACCOUNT_ASSET_TOGGLE:
            return self.account_asset_categories

        cities = self.city_ids

        account_asset_categories = {}

        account_journal_dict = {}
        for journal in self.journals_ids:
            if journal.code != "IMMO":
                continue
            account_journal_dict[journal.company_id[0]] = journal

        account_account_dict = {}
        for account in self.city_account_account_ids:
            _key = f"{account.company_id[0]}-{account.code}"
            account_account_dict[_key] = account

        with open(const.settings.ACCOUNT_ASSET_FILE, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if row.get("FE") and row.get("FE") != "#N/A":
                    carbon_id = self.env.ref(row.get("FE"))
                for city in cities:
                    account_account_id = account_account_dict.get(
                        f"{city.id}-{row['Code']}"
                    )

                    if account_account_id:
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
                            if row.get("FE") and row.get("FE") != "#N/A"
                            else {}
                        )

                        account_account_depreciation_id = self.env[
                            "account.account"
                        ].create(vals)

                        journal_id = account_journal_dict[city.id]

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

                        account_asset_categories[account_account_id.id] = cat.id

        self.account_asset_categories = account_asset_categories

        return self.account_asset_categories

    def populate_account_asset(self):
        if not const.settings.ACCOUNT_ASSET_TOGGLE:
            return self.account_asset

        categories = self.account_asset_categories

        account_asset_ids = []

        for lines in self.account_move_line_ids:
            lines_name = lines.name

            if (
                lines_name.startswith("20")
                or lines_name.startswith("21")
                and lines.debit > 0
            ):
                year = datetime.datetime.strptime(lines.date, "%Y-%m-%d").strftime("%Y")
                profile_id = categories.get(lines.account_id[0])
                account_asset = {
                    "name": lines_name + "." + year,
                    "purchase_value": lines.debit,
                    "date_start": str(int(year)) + "-01-01",
                    "company_id": lines.company_id[0],
                    "profile_id": profile_id,
                }
                account_asset_ids.append(account_asset) if profile_id else None

        if len(account_asset_ids) > 0:
            ids = self.env["account.asset"].create(account_asset_ids)

            ids.read(fields=[k for k, v in account_asset_ids[0].items()])

            # for index, account_asset in enumerate(account_asset_ids):
            #     account_asset["id"] = ids.ids[index]

            self.env["account.asset"].browse(ids.ids).validate()

        self.account_asset = account_asset_ids

        return self.account_asset

    def account_asset_create_move(self):
        if not const.settings.ACCOUNT_ASSET_TOGGLE:
            return False

        account_asset_line_ids = self.env["account.asset.line"].search(
            [
                ("line_days", "!=", 0),
                ("init_entry", "=", False),
                ("type", "=", "depreciate"),
            ]
        )

        line_ids = [element["id"] for element in account_asset_line_ids]

        chunk_number = (len(line_ids) // const.settings.ACCOUNT_ASSET_CHUNK_SIZE) + 1
        for i in range(chunk_number):
            logger.debug("Account Asset Create Move {}/{}".format(i + 1, chunk_number))
            account_ids = line_ids[
                const.settings.ACCOUNT_ASSET_CHUNK_SIZE
                * i : const.settings.ACCOUNT_ASSET_CHUNK_SIZE
                * (i + 1)
            ]
            self.env["account.asset.line"].browse(account_ids).create_move()

        return True
