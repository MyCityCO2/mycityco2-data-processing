import functools
import time

import typer
from loguru import logger
from multiprocess.pool import Pool

from . import runner

cli = typer.Typer(no_args_is_help=True)

instance_number = 7
instance_limit = 40
instance = list(range(0, instance_number * instance_limit, instance_limit))


@cli.command()
def run():
    start_time = time.perf_counter()
    # city = ["Fillière"]
    # city = ["La Roche-sur-Foron"]
    departement = 74
    func = functools.partial(
        runner.init,
        dataset=[],
        # dataset=utils.retreive_dataset(city),
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

    # except Exception as e:
    #     print(e)
    #     logger.error(e)

    # Merging csv #
    # logger.info("Merging CSV")
    # _path = const.settings.PATH / "data" / "temp_file"

    # dataframe = pandas.DataFrame()

    # csv_files = os.listdir(_path.resolve().as_posix())

    # if len(csv_files) > 1:
    #     for file in csv_files:
    #         if file.startswith("-".join(const.settings.ENV_DB.split("-")[:2])):
    #             path = _path + file

    #             csvfile = pandas.read_csv(path)
    #             dataframe = dataframe.append(csvfile, ignore_index=True)

    #             os.remove(path)

    #     dataframe.to_csv(
    #         f"{_path.as_posix()}/do-not-join-{const.settings.ENV_DB}.csv", index=False
    #     )

    #     logger.info("CSV Merged")
    # Merging csv #

    # else:
    #     logger.info("Finding one file, no merging")

    end_time = time.perf_counter()

    final_time = end_time - start_time

    logger.error(
        f"All took {final_time} secondes / {final_time / 60} minutes to execute"
    )


@cli.callback()
def callback():
    """
    MyCityCo2 data processing script
    """
