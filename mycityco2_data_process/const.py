from enum import Enum, unique
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, root_validator

_path = Path(__file__).absolute().parent


# TODO: Remove ENV_ before each settings
class Settings(BaseSettings):
    class Config:
        env_prefix = "MCO2DP_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    PATH = _path

    LOGORU_FORMAT: str = "<green>{time:YYYY-MM-DD at HH:mm:ss}</green> <level>{level}</level> - {message}"
    LOGURU_LEVEL: str = "DEBUG"

    # Rename DELETE_DB and remove from here and add to cli argument
    ENV_DELETE_DB_TOGGLE: bool = True

    ENV_URL: Optional[str]
    ENV_TEMPLATE_DB: Optional[str]
    ENV_DB: Optional[str]
    ENV_USERNAME: Optional[str]
    ENV_PASSWORD: Optional[str]
    ENV_MASTER_PASSWORD: Optional[str]

    CITY_CHUNK_SIZE: int = 1000
    ACCOUNT_CHUNK_SIZE: int = 6000
    ACCOUNT_ASSET_CHUNK_SIZE: int = 2000

    # Remove from here and add to FrImporter
    CARBON_FILE: str = (_path / "data/fr/fr_mapping_coa_exiobase.csv").as_posix()

    # Remove from here and add to FrImporter
    ACCOUNT_ASSET_TOGGLE: bool = True
    ACCOUNT_ASSET_FILE: str = (
        _path / "data/fr/fr_mapping_immo_exiobase.csv"
    ).as_posix()

    YEAR: list = list(range(2010, 2022))
    # YEAR: list = [2021]
    DEFAULT_ACCOUNT_TYPE: str = "off_balance"

    # Change to Export Operation Mode [local, distant]
    SQL_PORT = 666
    # TODO: Operation mode, find other way
    SQL_LOCAL = False

    ERROR_COUNTER = 0

    # Method
    @classmethod
    @root_validator()
    def prevent_none(cls, fields):
        for k, v in fields.items():
            if v is None:
                raise ValueError(f"The fields '{k}' must not be None")
        return fields


settings = Settings()


@unique
class LogLevels(str, Enum):
    ftrace = "ftrace"  # Otools-RPC (https://pypi.org/project/otools-rpc/)
    trace = "trace"
    debug = "debug"
    info = "info"
    success = "success"
    warning = "warning"
    error = "error"
    critical = "critical"

    def __str__(self):
        return self.value


@unique
class ImporterList(str, Enum):
    france = "fr"

    def __str__(self):
        return self.value
