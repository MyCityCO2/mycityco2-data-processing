import json

import psycopg2
import requests
from loguru import logger

from mycityco2_data_process import const


def change_superuser_state(dbname: str, state: bool = False) -> int:
    # DB #

    with psycopg2.connect(
        database=dbname,
        port=const.settings.SQL_PORT,
        host="localhost",
        password="odoo",
        user="odoo",
    ) if const.settings.SQL_LOCAL else psycopg2.connect(
        database=dbname, port=const.settings.SQL_PORT, host="/tmp", user="odoo"
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

    res = requests.get(dataset_url)

    content = res.content.decode("utf8")

    data = json.loads(content).get("records")

    dataset = []
    
    wanted_fields = ['com_name', 'com_siren_code']

    for city in data:
        city_field = city.get("fields")
        if city_field.get("com_name") in cities:
            city_dict = {'fields': {}}
            for k, v in city_field.items():
                if k in wanted_fields:
                    city_dict['fields'][k] = v
                    
            dataset.append(city_dict)
            
    return dataset
