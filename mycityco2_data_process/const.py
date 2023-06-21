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

    NTFY_TOGGLE: bool = False
    NTFY_LEVEL: str = "ERROR"
    NTFY_TOPICS: list[str] = ["opennetabo"]
    NTFY_TITLE: str = "MyCityCO2 Importer"
    NTFY_SERVER: str = "https://ntfy.sh/"

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

    CARBON_FILE: str = (_path / "data/fr/fr_mapping_coa_exiobase.csv").as_posix()

    ACCOUNT_ASSET_TOGGLE: bool = True
    ACCOUNT_ASSET_FILE: str = (
        _path / "data/fr/fr_mapping_immo_exiobase.csv"
    ).as_posix()

    YEAR: list = list(range(2010, 2022))
    DEFAULT_ACCOUNT_TYPE: str = "off_balance"

    SQL_PORT = 666
    SQL_LOCAL = False

    ERROR_COUNTER = 0

    # Method
    @root_validator()
    def prevent_none(cls, fields):
        for k, v in fields.items():
            if v is None:
                raise ValueError(f"The fields '{k}' must not be None")
        return fields


settings = Settings()
