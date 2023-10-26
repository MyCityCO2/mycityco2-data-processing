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
    YEARS_TO_COMPUTE: list = list(range(2010, 2023))
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

    REQUIRED_ODOO_MODULE = [
        "onsp_co2_account_asset_management",
        "account_asset_management",
        "onsp_co2",
    ]

    # module_name, git link (with .git at the end), branch
    GIT_MODULE: list[tuple] = [
        (
            "onsp_co2_bundle",
            "git@github.com:MyCityCO2/mycityco2-engine.git",
            "16.0",
        ),
        (
            "account-financial-tools",
            "git@github.com:OCA/account-financial-tools.git",
            "16.0",
        ),
        ("reporting-engine", "git@github.com:OCA/reporting-engine.git", "16.0"),
    ]
    GIT_PATH = _path / "data" / "common" / "modules"

    # Docker parameters
    DOCKER_CONTAINER_START_NAME: str = "mycityco2_container_"
    DOCKER_ODOO_CONTAINER_NAME: str = DOCKER_CONTAINER_START_NAME + "odoo"
    DOCKER_POSTGRES_CONTAINER_NAME: str = DOCKER_CONTAINER_START_NAME + "db"

    DOCKER_NETWORK_NAME: str = "mycityco2_network"

    DOCKER_ODOO_IMAGES: str = "odoo:16.0"
    DOCKER_POSTGRES_IMAGES: str = "postgres:13"

    ODOO_CONF_PATH: Path = PATH / "data" / "common" / "odoo.conf"

    OPERATION_MODE: str = "docker"

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
