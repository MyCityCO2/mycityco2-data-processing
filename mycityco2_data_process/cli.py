import functools
import os
import time

import pandas
import typer
from loguru import logger
from multiprocess.pool import Pool

from mycityco2_data_process import const

from . import runner, utils

cli = typer.Typer(no_args_is_help=True)

instance_number = 1
instance_limit = 40
instance = list(range(0, instance_number * instance_limit, instance_limit))


@cli.command()
def run():
    start_time = time.perf_counter()
    city = ["La Roche-sur-Foron"]
    departement = 74
    func = functools.partial(
        runner.init,
        dataset=utils.retreive_dataset(city),
        instance=instance,
        instance_number=instance_number,
        instance_limit=instance_limit,
        departement=departement,
    )
    try:
        with Pool(instance_number) as p:
            p.map(func, instance)

    except KeyboardInterrupt:
        logger.info("Ctrl-c entered. Exiting")

    except Exception as e:
        print(e)
        logger.error(e)

    # Merging csv #
    logger.info("Merging CSV")
    _path = "temp_file/"

    dataframe = pandas.DataFrame()

    csv_files = os.listdir(_path)

    if len(csv_files) > 1:
        for file in csv_files:
            if file.startswith("-".join(const.settings.ENV_DB.split("-")[:2])):
                path = _path + file

                csvfile = pandas.read_csv(path)
                dataframe = dataframe.append(csvfile, ignore_index=True)

                os.remove(path)

        dataframe.to_csv(
            f"temp_file/do-not-join-{const.settings.ENV_DB}.csv", index=False
        )

        logger.info("CSV Merged")
        # Merging csv #

        # SENDING DISCORD#
        # from discord_webhook import DiscordWebhook

        # webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1117834229154324591/WZ-LFSF9_g0ZDAhHukKJguJB8UI1liBB_21U7iktOkvG7QopB_As5XA5Bnk9Dj_OTBAb", username="Importer Files")

        # with open(f'temp_file/{const.settings.ENV_DB}.csv', "rb") as f:
        #     webhook.add_file(file=f.read(), filename="importer.csv")

        # response = webhook.execute()
        # SENDING DISCORD#
    else:
        logger.info("Finding one file, no merging")

    end_time = time.perf_counter()

    final_time = end_time - start_time

    logger.error(
        f"All took {final_time} secondes / {final_time / 60} minutes to execute"
    )

    # logger.critical("AU SECOURS BCH VIENT M'AIDER")


@cli.callback()
def callback():
    """
    MyCityCo2 data processing script
    """
