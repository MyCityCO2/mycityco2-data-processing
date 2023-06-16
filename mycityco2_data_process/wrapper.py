from loguru import logger
from otools_rpc.external_api import Environment

from mycityco2_data_process import const


class CustomEnvironment:
    # _self = None

    # def __new__(cls, hey):
    #     # if cls._self is None:
    #     cls._self = super().__new__(cls)
    #     return cls._self

    def __init__(self, dbname=const.settings.ENV_DB):
        self.env = Environment(
            url=const.settings.ENV_URL,
            username=const.settings.ENV_USERNAME,
            password=const.settings.ENV_PASSWORD,
            db=dbname,
            auto_auth=False,
            logger=logger,
        )
