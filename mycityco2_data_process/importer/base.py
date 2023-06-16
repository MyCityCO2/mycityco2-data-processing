import fnmatch
import time
from abc import ABC, abstractmethod

import pandas
import psycopg2
from loguru import logger
from otools_rpc.external_api import Environment

from mycityco2_data_process import const


class AbstractImporter(ABC):
    """Default class. This class is used to be the parent of the other Importer. You need to inherit this class in order to be able to create an importer"""

    # DECORATOR
    def time(fn):
        """This decorator allow you to get the time the function take to run. Not useful in prod, but it is in dev."""

        def wrapper(self, *args, **kwargs):
            start_time = time.perf_counter()
            function = fn(self, *args, **kwargs)
            end_time = time.perf_counter()

            final_time = end_time - start_time

            logger.debug(
                f"{fn.__name__} took {final_time} secondes / {final_time / 60} minutes to execute"
            )

            return function

        return wrapper

    def depends(*fields):
        """Allow you to depends on certain object attribute, you can easily do @depends('city_ids', 'city_account_account_ids') and you will depends on multiple attribute."""

        def decorator(fn):
            def wrapper(self, *args, **kwargs):
                for field in fields:
                    if not getattr(self, field, None):
                        raise AttributeError(
                            f"Fields '{field}' does not exist in '{fn.__name__}'."
                        )

                return fn(self, *args, **kwargs)

            return wrapper

        return decorator

    def _create_by_chunk(
        self, model: str = "", vals_list: list = [], chunk: int = 1000
    ):
        """Create vals from an list to an model by chunk, useful to bypass overflow error."""
        if len(model.split(".")) < 2:
            raise AttributeError(f"Model '{model}' is not a valid model")

        vals_list_id = self.env[model]

        chunk_number = (len(vals_list) // chunk) + 1
        for i in range(chunk_number):
            logger.debug(
                f"Creating '{model}' chunk {i + 1}/{chunk_number}. Chunk size {chunk}."
            )
            created_city = self.env[model].create(
                vals_list[chunk * i : chunk * (i + 1)]
            )

            vals_list_id |= created_city

        logger.debug(f"All {model} chunk has been created")
        return vals_list_id

    def __init__(self, env):
        """Initialize the object from an Environment."""
        self.env: Environment = env
        self.user_ids: any = self.env["res.users"].search_read([])
        self.currency_id: any = self.env["res.currency"].search_read(
            [("name", "=", self.currency_name)]
        )
        self.external_layout_id: any = self.env.ref("web.external_layout_standard")

        self.city_ids: any = None
        self.city_account_account_ids: any = None
        self.account_account_ids: any = None
        self.account_move_ids: any = None
        self.account_move_line_ids: any = None
        self.carbon_factor: list[dict[str, str, str]] = None
        self.carbon_factor_id: list[dict[str, any]] = {}
        self.account_asset_categories: dict = {}
        self.account_asset: any = None

    @abstractmethod
    def source_name(self):
        """This need to return an string, you may choose what in the string but we'll do 'API', 'DOCX'"""
        raise NotImplementedError()

    @abstractmethod
    def currency_name(self):
        """Allow us to get the currency. You'll need to return an string like 'EUR'"""
        raise NotImplementedError()

    @abstractmethod
    def get_cities(self):
        """This function is how we can get the city data.

        return format: list[dict['district', 'name']] #At least those two variable. Those shall be unique.
        ex: [{'district': '12', 'name': 'Lausanne'}, {'district': '13', 'name': 'Geneve'}]
        """
        raise NotImplementedError()

    @abstractmethod
    def get_journal_data(self):
        """This function will generate an pattern for the account.journal. In this function you'll need to iterate on all city and generate journal according and return them without any creation."""
        raise NotImplementedError()

    @abstractmethod
    def get_account_account_data(self):
        """This function shall return the account.account data without any creation."""
        raise NotImplementedError()

    @abstractmethod
    def get_account_move_data(self, registry):
        """This function shall return the account.move data without any creation."""
        raise NotImplementedError()

    @depends("external_layout_id", "user_ids", "currency_id")
    def cities_data_list(self):
        """This function use our get_cities data to parse our old data to newer one."""
        cities = self.get_cities()

        res_city_vals_list = [
            {
                "currency_id": self.currency_id.id,
                "name": city.get("name"),
                "company_registry": city.get("district", False),
                "user_ids": self.user_ids.ids,
                "external_report_layout_id": self.external_layout_id.id,
                "carbon_in_compute_method": "monetary",  # IN Future, NOT NEEDED
                "carbon_out_compute_method": "monetary",  # IN Future, NOT NEEDED
            }
            for city in cities
        ]

        return res_city_vals_list

    def populate_journal(self):
        """This function is only there to create all our get_journal_data in Odoo"""
        journals_ids = self.get_journal_data()

        journals = self.env["account.journal"].create(journals_ids)

        self.journals_ids = journals

        return journals_ids

    def populate_cities(self):
        """This function is only there to create all our cities_data_list in Odoo. One city correspond to one Odoo company."""
        city_vals_list = self.cities_data_list()

        cities = self._create_by_chunk(
            "res.company", city_vals_list, const.settings.CITY_CHUNK_SIZE
        )

        self.city_ids = cities

        return cities

    def populate_account_account(self):
        """Populate the account data with the data in the chart."""
        account_account_ids = self.get_account_account_data()

        accounts = self._create_by_chunk(
            "account.account", account_account_ids, const.settings.ACCOUNT_CHUNK_SIZE
        )

        self.city_account_account_ids = accounts

        return accounts

    def create_account_move(self, vals):
        """This function is there to create account.move"""

        account_move_id = self.env["account.move"].create(vals)

        return account_move_id

    @depends("account_account_ids")
    def populate_account_move(self):
        """This function is only there to iterate on the create of account.move data."""

        account_move_list = self.get_account_move_data()

        # logger.error([elem.get('company_id') for elem in account_move_list])

        # account_move_ids = self.env['account.move.line'].create(account_move_list)

        # logger.debug(f"Data sent for {', '.join(self.city_ids.mapped('name'))} for {', '.join(const.settings.YEAR)}")

        self.env["account.move"].search(
            [("amount_total_signed", "!=", 0)]
        ).action_post()

        # self.account_move_line_ids = account_move_ids

    def export_data(self):
        co2_categories = [
            {"id": 1, "code": "MAI", "name": "Maintenance"},
            {"id": 2, "code": "CON", "name": "Construction"},
            {"id": 3, "code": "INS", "name": "Installations"},
            {"id": 4, "code": "TRP", "name": "Transports"},
            {"id": 5, "code": "FLU", "name": "Fluides (Energie, Eau...)"},
            {"id": 6, "code": "SER", "name": "Services"},
            {"id": 7, "code": "FOU", "name": "Fournitures"},
            {"id": 8, "code": "OTH", "name": "Autres"},
            {"id": 9, "code": "ALI", "name": "Alimentation"},
            {"id": 10, "code": "TAX", "name": "Impots et cotisations"},
        ]

        coa_condition = sorted(
            [
                {"condition": "6*", "category_id": 8, "rule_order": 999},
                {"condition": "66*", "category_id": 6, "rule_order": 200},
                {"condition": "61*", "category_id": 6, "rule_order": 200},
                {"condition": "62*", "category_id": 6, "rule_order": 200},
                {"condition": "64*", "category_id": 10, "rule_order": 200},
                {"condition": "63*", "category_id": 10, "rule_order": 200},
                {"condition": "615*", "category_id": 1, "rule_order": 100},
                {"condition": "60622*", "category_id": 4, "rule_order": 100},
                {"condition": "625*", "category_id": 4, "rule_order": 100},
                {"condition": "6811.21*", "category_id": 2, "rule_order": 100},
                {"condition": "61551*", "category_id": 4, "rule_order": 100},
                {"condition": "624*", "category_id": 4, "rule_order": 100},
                {"condition": "6064*", "category_id": 8, "rule_order": 100},
                {"condition": "6065*", "category_id": 8, "rule_order": 100},
                {"condition": "6067*", "category_id": 8, "rule_order": 100},
                {"condition": "6068*", "category_id": 8, "rule_order": 100},
                {"condition": "60621*", "category_id": 5, "rule_order": 100},
                {"condition": "6063*", "category_id": 1, "rule_order": 100},
                {"condition": "6811.204*", "category_id": 2, "rule_order": 50},
                {"condition": "6811.203*", "category_id": 6, "rule_order": 50},
                {"condition": "6811.215*", "category_id": 3, "rule_order": 50},
                {"condition": "6811.202*", "category_id": 6, "rule_order": 50},
                {"condition": "6042*", "category_id": 6, "rule_order": 50},
                {"condition": "6574", "category_id": 6, "rule_order": 50},
                {"condition": "60623", "category_id": 9, "rule_order": 10},
                {"condition": "60613", "category_id": 5, "rule_order": 10},
                {"condition": "6061*", "category_id": 5, "rule_order": 10},
                {"condition": "60612", "category_id": 5, "rule_order": 10},
                {"condition": "6811.2182", "category_id": 4, "rule_order": 10},
            ],
            key=lambda k: k["rule_order"],
        )

        connection = (
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
        logger.debug("Extracting data from ODOO, using SQL")
        dataframe = pandas.read_sql_query(query, connection)

        ### Habitant ###
        logger.debug("Matching habitant/postal code to city")
        siren_to_habitant = pandas.read_csv("static/fr/siren.csv")
        siren_to_postal = pandas.read_csv("static/fr/postal.csv")

        siren_to_postal = siren_to_postal.groupby(["insee"]).agg(lambda x: list(x))

        print(siren_to_postal)

        city_data = pandas.merge(
            siren_to_habitant,
            siren_to_postal,
            how="inner",
            left_on="insee",
            right_on="insee",
        )

        dataframe["city_id"] = dataframe["city_id"].astype(int)

        dataframe = pandas.merge(
            dataframe, city_data, how="left", left_on="city_id", right_on="siren"
        )

        dataframe["city_id"] = dataframe["city_id"].astype(int)

        # def habitant(siren):
        #     if siren:
        #         commune = city_data.where(city_data['siren'] == int(siren))

        #         return commune.loc[commune.first_valid_index()].get('pmun_2023')
        #     return 0

        # def zip_code(siren):
        #     if siren:
        #         commune = city_data.where(city_data['siren'] == int(siren))

        #         return commune.loc[commune.first_valid_index()].get('postal')
        #     return 0
        # dataframe['habitant'] = dataframe['city_id'].apply(habitant)
        # dataframe['city_zip_code'] = dataframe['city_id'].apply(zip_code)
        ### Habitant ###

        ### Category ###
        logger.debug("Matching Category to account.account")

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

        dataframe["category_tuple"] = dataframe["category_id"].apply(find_categories)

        dataframe["category_code"] = dataframe["category_tuple"].apply(unpack_code)
        dataframe["category_name"] = dataframe["category_tuple"].apply(unpack_name)

        dataframe = dataframe.drop(columns=["category_id", "category_tuple"])

        dataframe = dataframe[dataframe["category_name"] != False]
        ### Category ###

        logger.debug("Computing Carbon per habitant")
        ### Carbon Factor ###
        # dataframe['entry_carbon_kgco2e_per_hab'] = dataframe['entry_carbon_kgco2e']/dataframe['habitant']
        ### Carbon Factor ###

        # dataframe = dataframe[['city_id', 'city_name', "account_code", 'account_name', 'journal_code', 'journal_name', 'entry_year', 'entry_amount']]

        print(dataframe)

        logger.debug("Sorting dataframe")
        dataframe = dataframe.sort_values(by=["city_id", "account_code", "entry_year"])

        logger.debug(f"Exporting dataframe to 'temp_file/{self._db}.csv'")
        dataframe.to_csv(f"temp_file/{self._db}.csv", index=False)
