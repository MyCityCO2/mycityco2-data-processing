import fnmatch
import os

import pandas
from loguru import logger
from mycityco2_data_process import const



DROP_COLUMNS = [
    'line_label',
    'label',
    'account',
    'emission_factor_name',
]


sorted_files = sorted([f.name for f in os.scandir(const.settings.DATA_PATH)])

for filename in sorted_files:
    if not fnmatch.fnmatch(filename, "*.csv"):
        continue
    logger.success(f"{filename} - Reading CSV")
    csv_file = pandas.read_csv(const.settings.DATA_PATH / filename)


    for col in DROP_COLUMNS:
        if col in csv_file.columns:
            csv_file = csv_file.drop(columns=[col])

    csv_file = csv_file.dropna(subset=['postal', 'account_code'])
    csv_file = csv_file.drop(csv_file[csv_file['account_code'] == 0].index)

    csv_file.to_csv(const.settings.CLEANED_PATH / filename, index=False)

