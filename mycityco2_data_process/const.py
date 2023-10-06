from enum import Enum, unique
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, root_validator

_path = Path(__file__).absolute().parent


class Settings(BaseSettings):
    class Config:
        env_prefix = "MCO2DP_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    PATH = _path

    LOGORU_FORMAT: str = "<green>{time:YYYY-MM-DD at HH:mm:ss}</green> <level>{level}</level> - {message}"
    LOGURU_LEVEL: str = "DEBUG"

    # Rename DELETE_DB and remove from here and add to cli argument
    DELETE_DB_TOGGLE: bool = True

    URL: Optional[str]
    TEMPLATE_DB: Optional[str]
    DB: Optional[str]
    USERNAME: Optional[str]
    PASSWORD: Optional[str]
    MASTER_PASSWORD: Optional[str]

    CITY_CHUNK_SIZE: int = 1000
    ACCOUNT_CHUNK_SIZE: int = 4000
    ACCOUNT_ASSET_CHUNK_SIZE: int = 2000

    # 2022 Only available in certain dataset for France
    YEAR: list = list(range(2010, 2023))
    # YEAR: list = [2010]
    DEFAULT_ACCOUNT_TYPE: str = "off_balance"

    NO_DELETE_DB = False

    # Change to Export Operation Mode [local, distant]
    SQL_PORT = 666
    # TODO: Operation mode, find other way
    SQL_LOCAL = False
    SQL_LOCAL_HOST = "localhost"
    SQL_LOCAL_PORT = 5432
    SQL_LOCAL_USER = False
    SQL_LOCAL_PASSWORD = False

    ERROR_COUNTER = 0

    # Directories paths
    TEMP_FILE_PATH = PATH / "data" / "temp_file"
    DATA_PATH = TEMP_FILE_PATH / "final_data"
    CLEANED_PATH = TEMP_FILE_PATH / "cleaned_data"
    ARCHIVE_PATH = TEMP_FILE_PATH / "archive"
    TMP_DATA = TEMP_FILE_PATH / "tmp_data"

    COMMON_FILE_PATH = PATH / "data" / "common"
    FACTOR_CARBON_MAPPED_FILE = COMMON_FILE_PATH / "carbon_factor_mapping.xlsx"

    REQUIRED_ODOO_MODULE = ["onsp_co2"]

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
