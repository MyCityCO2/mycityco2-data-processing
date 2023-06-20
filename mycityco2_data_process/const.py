from pathlib import Path

from pydantic import BaseSettings

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
    ENV_URL: str = "https://tests-odoo-16c.odooapps.ch"
    ENV_TEMPLATE_DB: str = "bch-mycity-co2-temlate-test"
    # ENV_DB: str = "bch-foron-departement"
    # ENV_URL: str = "http://172.25.0.3:8069"
    # ENV_TEMPLATE_DB: str = 'template'
    ENV_DB: str = "temp-departement-cli-testing"
    ENV_USERNAME: str = "__system__"
    # todo: add validator and make it optional
    ENV_PASSWORD: str
    ENV_MASTER_PASSWORD: str

    CITY_CHUNK_SIZE: int = 1000
    ACCOUNT_CHUNK_SIZE: int = 6000
    ACCOUNT_ASSET_CHUNK_SIZE: int = 2000

    CARBON_FILE: str = (_path / "data/fr/fr_mapping_coa_exiobase.csv").as_posix()

    ACCOUNT_ASSET_TOGGLE: bool = True
    ACCOUNT_ASSET_FILE: str = (
        _path / "data/fr/fr_mapping_immo_exiobase.csv"
    ).as_posix()

    YEAR: list = list(range(2010, 2022))
    # YEAR: list = [2021]
    DEFAULT_ACCOUNT_TYPE: str = "off_balance"

    # SKIPPED_CITY: str = ['Allinges', 'Amancy']
    SKIPPED_CITY: list[str] = []

    SQL_PORT = 666
    SQL_LOCAL = False
    # SQL_PORT = 667


settings = Settings()
