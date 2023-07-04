import fnmatch
import os
import sys

import pandas
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO".upper())

PATH = "./files"

REQUIRED_COLUMNS = [
    "city_id",
    "city_name",
    "account_code",
    "account_name",
    "account",
    "journal_code",
    "journal_name",
    "entry_year",
    "entry_amount",
    "entry_currency",
    "entry_carbon_kgco2e",
    "emission_factor_name",
    "postal",
    "category_code",
    "category_name",
]

ERROR_FILE = []

WARNING_YEAR = list(range(2016, 2022))

STEP = {"1": True, "2": True, "3": True}

step3_city = []

for file in os.scandir(PATH):
    if not fnmatch.fnmatch(file.name, "*.csv"):
        continue
    logger.success(f"{file.name} - Reading CSV")
    csv_file = pandas.read_csv(PATH + "/" + file.name)

    file_error_count = 0

    # Step 1
    if STEP.get("1"):
        if csv_file.columns.to_list() == REQUIRED_COLUMNS:
            logger.info(f"{file.name} - STEP 1: OK")

        else:
            logger.error(f"{file.name} - STEP 1: NOT OK")
            file_error_count = +1
            differencies = list(set(csv_file.columns.to_list()) - set(REQUIRED_COLUMNS))
            if differencies:
                logger.error(
                    f"{file.name} - Colums '{', '.join(differencies)}' shall not be there"
                )
            else:
                logger.error(f"{file.name} - Missing columns")
                continue
    # Step 1

    # Step 2
    step2_error = 0
    if STEP.get("2"):

        def check_if_not_none(row):
            global step2_error
            if str(row) in ("", "nan"):
                step2_error = +1

        for fields in REQUIRED_COLUMNS:
            if fields == "postal":
                continue
            csv_file[fields].apply(check_if_not_none)

        if step2_error >= 1:
            logger.error(f"{file.name} - STEP 2: NOT OK")
            continue
        logger.info(f"{file.name} - STEP 2: OK")
    # Step 2

    # Step 3
    if STEP.get("3"):
        city_name = csv_file["city_name"].unique()

        for name in city_name:
            city_df = csv_file[csv_file["city_name"] == name]

            years = [int(year) for year in city_df["entry_year"].unique()]

            for year in WARNING_YEAR:
                if year not in years:
                    step3_city.append(f"{name}|-|{year}")
                    logger.debug(
                        f"{file.name} - The City '{name}' don't have any account.move for '{year}'"
                    )

        if step3_city:
            logger.warning(f"{file.name} - STEP 3: NOT OK (WARNING)")
        else:
            logger.info(f"{file.name} - STEP 3: OK")
    # Step 3

    if file_error_count >= 1:
        logger.error(f"File '{file.name}' has {file_error_count} errors")
        ERROR_FILE.append(file.name)

for data in step3_city:
    if ERROR_FILE:
        break

    name, year = data.split("|-|")

    logger.warning(f"The City '{name}' don't have any account.move for '{year}'")


for file in ERROR_FILE:
    logger.error(f"File '{file}' has errors")
