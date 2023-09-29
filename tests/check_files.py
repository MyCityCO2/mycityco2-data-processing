import os
from loguru import logger
from mycityco2_data_process import const



sorted_directories = sorted([d.name for d in os.scandir(const.settings.ARCHIVE_PATH)])

for directory in sorted_directories:
    files = os.scandir(const.settings.ARCHIVE_PATH + "/" + directory)

    files_qty = len(list(files))
    if files_qty != 7:
        logger.error(f"{directory} - {files_qty} files")
