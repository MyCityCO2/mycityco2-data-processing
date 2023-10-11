import time
from abc import ABC, abstractmethod
from typing import Any

import pandas
import typer
from loguru import logger
from otools_rpc.external_api import Environment

from mycityco2_data_process import const


# DECORATOR
def timer(fn):
    """This decorator allow you to get the time the function take to run. Not useful in prod, but it is in dev."""

    def wrapper(self, *args, **kwargs):
        start_time = time.perf_counter()
        function = fn(self, *args, **kwargs)
        end_time = time.perf_counter()

        final_time = end_time - start_time

        logger.debug(
            f"{self._db} - {fn.__name__} took {final_time} secondes / {final_time / 60} minutes to execute"
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


class AbstractImporter(ABC):
    """Default class. This class is used to be the parent of the other Importer. You need to inherit this class in order to be able to create an importer"""

    def _create_by_chunk(
        self, model: str = "", vals_list: list = [], chunk: int = 1000
    ):
        """Create vals from an list to an model by chunk, useful to bypass overflow error."""
        vals_list_id = self.env[model]

        chunk_number = (len(vals_list) // chunk) + 1
        for i in range(chunk_number):
            logger.debug(
                f"{self._db} - Creating '{model}' chunk {i + 1}/{chunk_number}. Chunk size {chunk}."
            )
            vals = vals_list[chunk * i : chunk * (i + 1)]
            vals_list_id = self.env[model].create(vals)

            # if vals:
            #     created_record.read(fields=[k for k, _ in vals[0].items()])

            # vals_list_id |= created_record

        logger.debug(f"{self._db} - All '{model}' chunk has been created")
        return vals_list_id

    def __init__(self, env: Environment = None, db: str = None):
        """Initialize the object from an Environment."""
        self.env: Environment = env
        self._db = db

        if not self.check_env():
            raise typer.Abort()

        self.user_ids: Any = self.env["res.users"].search_read([])
        self.currency_id: Any = self.env["res.currency"].search_read(
            [("name", "=", self.currency_name)]
        )
        self.external_layout_id: Any = self.env.ref("web.external_layout_standard")

        # TODO: replace Any by recordset type

        self.city_ids: Any = self.env["res.company"]
        self.city_account_account_ids: Any = self.env["account.account"]
        self.account_account_ids: Any = self.env["account.account"]
        self.account_move_ids: Any = self.env["account.move"]
        self.account_move_line_ids: Any = self.env["account.move.line"]
        self.carbon_factor: list[dict[str, str, str]] = None
        self.carbon_factor_id: list[dict[str, Any]] = {}
        self.account_asset_categories: dict = {}
        self.account_asset: Any = self.env["account.asset"]

        self.init_step()

    def init_step(self):
        self.step1_1 = 0
        self.step1_2 = 0
        self.step2_3 = 0

        self.step2_1 = 0
        self.step2_2 = 0

        self.step3_1 = 0
        self.step3_2 = 0
        self.step3_3 = 0

        self.step4_1 = 0
        self.step4_2 = 0
        self.step4_3 = 0
        self.step4_4 = 0
        self.step4_5 = 0
        self.step4_6 = 0

    def check_env(self):
        # Checking required module
        for module_name in const.settings.REQUIRED_ODOO_MODULE:
            module = self.env["ir.module.module"].search_read(
                [("name", "=", module_name)]
            )

            if module.state != "installed":
                logger.error(
                    "Please install the module '{0}' on the db '{1}' since it's required".format(
                        module.name, const.settings.TEMPLATE_DB
                    )
                )
                return False

        # Checking and activating currency
        currency = self.env["res.currency"].search_read(
            [("name", "=", self.currency_name), ("active", "in", [True, False])]
        )
        if not currency:
            logger.error("Please select a existing currency")
            return False
        if not currency.active:
            currency.write({"active": True})

        # Carbon Factor
        carbon_factor = []
        # carbon_factor = self.env["carbon.factor"].search_read([])
        if not len(carbon_factor):
            logger.info("Creating Carbon Factor Records")
            factor_carbon_mapping_df = pandas.DataFrame(
                pandas.read_excel(const.settings.FACTOR_CARBON_MAPPED_FILE)
            )
            lis = factor_carbon_mapping_df.groupby(
                by=["Id", "Sector"], group_keys=False
            ).apply(lambda row: list(zip(list(row["Year"]), list(row["GES"]))))

            factor_vals_list = []
            xml_id_vals_list = []

            EUR = self.env.ref("base.EUR")
            for a, b in list(zip(lis.index, lis)):
                xml_id, factor_name = a
                factor_vals_list.append(
                    {
                        "name": factor_name,
                        "carbon_compute_method": "monetary",
                        "value_ids": [
                            (
                                0,
                                0,
                                {
                                    "date": f"{year}-01-01",
                                    "carbon_value": round(value / 1_000_000, 6),
                                    "carbon_monetary_currency_id": EUR.id,
                                    "source": "Exiobase",
                                },
                            )
                            for year, value in b
                        ],
                    }
                )

                model, name = xml_id.split(".")
                xml_id_vals_list.append(
                    {
                        "module": model,
                        "name": name,
                        "model": ".".join(model.split("_")),
                    }
                )

            factor_ids = self.env["carbon.factor"].create(factor_vals_list)

            for factor_id, xml_id_vals in list(zip(factor_ids, xml_id_vals_list)):
                xml_id_vals["res_id"] = factor_id.id

            self.env["ir.model.data"].create(xml_id_vals_list)

        # logger.error("here")
        # logger.error(
        #     self.env["res.users"]
        #     .search([("login", "=", "__system__")])
        #     .write({"password": "abo"})
        # )
        # logger.error("here")
        return True

    @abstractmethod
    def source_name(self):
        """This need to return an string, you may choose what in the string but we'll do 'API', 'DOCX'"""
        raise NotImplementedError()

    @abstractmethod
    def importer(self):
        """This need to return an string, you may choose what in the string but we'll do 'fr', 'ch'"""
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
    def get_account_move_data(self):
        """This function shall return the account.move data without any creation."""
        raise NotImplementedError()

    @depends("external_layout_id", "user_ids", "currency_id")
    def cities_data_list(self):
        """This function use our get_cities data to parse our old data to newer one."""
        step1_1_start_timer = time.perf_counter()
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
        step1_1_end_timer = time.perf_counter()

        self.step1_1 += step1_1_end_timer - step1_1_start_timer

        return res_city_vals_list

    def populate_journal(self):
        """This function is only there to create all our get_journal_data in Odoo"""
        journals_ids = self.get_journal_data()

        journals = self.env["account.journal"].create(journals_ids)

        if len(journals_ids):
            journals.read(fields=[k for k, v in journals_ids[0].items()])

        self.journals_ids = journals

        return journals_ids

    def populate_cities(self):
        """This function is only there to create all our cities_data_list in Odoo. One city correspond to one Odoo company."""
        city_vals_list = self.cities_data_list()

        step1_2_start_timer = time.perf_counter()

        cities = self._create_by_chunk(
            "res.company", city_vals_list, const.settings.CITY_CHUNK_SIZE
        )

        self.city_ids = cities
        step1_2_end_timer = time.perf_counter()

        self.step1_2 += step1_2_end_timer - step1_2_start_timer

        return cities

    def populate_account_account(self):
        """Populate the account data with the data in the chart."""
        account_account_ids = self.get_account_account_data()

        step2_3_start_timer = time.perf_counter()

        accounts = self._create_by_chunk(
            "account.account", account_account_ids, const.settings.ACCOUNT_CHUNK_SIZE
        )

        self.city_account_account_ids = accounts
        step2_3_end_timer = time.perf_counter()

        self.step2_3 += step2_3_end_timer - step2_3_start_timer

        return accounts

    def create_account_move(self, vals_list: list):
        """This function is there to create account.move"""
        account_move_id = self.env["account.move"].create(vals_list)

        if len(vals_list):
            account_move_id.read(fields=[k for k, _ in vals_list[0].items()])

        self.account_move_ids |= account_move_id

        return account_move_id

    @depends("account_account_ids")
    def populate_account_move(self):
        """This function is only there to iterate on the create of account.move data."""
        self.get_account_move_data()
