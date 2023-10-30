import json
import os
import time

import psycopg2
import requests
from git import Repo
from loguru import logger

from mycityco2_data_process import const
from mycityco2_data_process.wrapper import CustomEnvironment


def change_superuser_state(dbname: str, state: bool = False) -> int:
    # DB #

    with psycopg2.connect(
        database=dbname,
        port=const.settings.SQL_LOCAL_PORT,
        host=const.settings.SQL_LOCAL_HOST,
        user=const.settings.SQL_LOCAL_USER,
        password=const.settings.SQL_LOCAL_PASSWORD,
    ) if const.settings.SQL_LOCAL else psycopg2.connect(
        database=dbname,
        port=const.settings.SQL_PORT,
        host="localhost",
        user="odoo",
        password="odoo",
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(f"update res_users set active = {state} where id = 1;")
        # DB #
        connection.commit()

        logger.debug(
            f"The database {dbname} have now the superuser '{'Enabled' if state else 'Disabled'}'"
        )
        return cursor.rowcount


def retreive_dataset(cities):
    dataset_url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-france-commune&q=&sort=com_name&rows=-1&start=0&refine.dep_code=74"

    res = requests.get(dataset_url, allow_redirects=False)

    content = res.content.decode("utf8")

    data = json.loads(content).get("records")

    dataset = []

    wanted_fields = ["com_name", "com_siren_code"]

    for city in data:
        city_field = city.get("fields")
        if city_field.get("com_name") in cities:
            city_dict = {"fields": {}}
            for k, v in city_field.items():
                if k in wanted_fields:
                    city_dict["fields"][k] = v

            dataset.append(city_dict)

    return dataset


def wait_for_odoo() -> bool:
    env = CustomEnvironment()
    while True:
        try:
            env.env.common.version()
            return True
        except (ConnectionRefusedError, ConnectionResetError):
            time.sleep(1)
            continue
        except Exception as err:
            logger.error(f"Odoo server not running {err}")
            return False


def clone_repos() -> bool:
    for module_name, link, branch in const.settings.GIT_REPOS:
        path = const.settings.GIT_PATH / module_name
        if not os.path.isdir(path):
            Repo.clone_from(
                link,
                path.as_posix(),
                branch=branch,
                depth=1,
            )


def ensure_temp_file():
    path = const.settings.TEMP_FILE_PATH
    if not os.path.isdir(path):
        os.makedirs(path)
