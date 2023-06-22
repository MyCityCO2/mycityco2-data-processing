import functools
import math
import os
import time

import pandas
import typer
from loguru import logger
from multiprocess.pool import Pool

from . import const, runner
from .importer.fr import get_departement_size

cli = typer.Typer(no_args_is_help=True)


# TODO: Add importer type argument using Class like (https://gitlab.open-net.ch/rzu/ons-docker/-/blob/master/ons_docker/cli/main.py#L56) same to our callback
@cli.command()
def run(
    departement: int = typer.Option(74, "--departement"),
    instance_number: int = typer.Option(7, "-i", "--instance"),
    instance_limit: int = typer.Option(0, "-l", "--limit"),
):
    instance_limit = (
        math.trunc(get_departement_size(departement) / instance_number) + 1
        if not instance_limit
        else instance_limit
    )
    instance = list(range(0, instance_number * instance_limit, instance_limit))

    # print(departement)
    # return
    start_time = time.perf_counter()
    # city = ["La Roche-sur-Foron"]
    # city = ["Scionzier"]
    # departement = 74
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
    #     logger.error(e)
    #     raise typer.Abort()

    # else:
    #     logger.info("Finding one file, no merging")

    end_time = time.perf_counter()

    final_time = end_time - start_time

    logger.success(
        f"All took {final_time} secondes / {final_time / 60} minutes to execute"
    )


# TODO: test merge command
@cli.command()
def csv(
    merge: bool = typer.Option(False, "-m", "--merge"),
    delete: bool = typer.Option(False, "-d", "--delete"),
    name: str = typer.Option("city_data", "-n", "--name"),
):
    if merge:
        # Merging csv #
        logger.info("Merging CSV")
        _path = const.settings.PATH / "data" / "temp_file"

        dataframe = pandas.DataFrame()

        csv_files = os.listdir(_path.resolve().as_posix())

        for file in csv_files:
            if file.endswith(".csv") and file.startswith("temp"):
                logger.info(f"Merging '{file}'")
                path = _path / file

                csvfile = pandas.read_csv(path.as_posix())
                dataframe = pandas.concat([dataframe, csvfile], ignore_index=True)

                if delete:
                    os.remove(path)

        dataframe.to_csv(f"{_path.as_posix()}/{name}.csv", index=False)

        logger.info("CSV Merged")
        # Merging csv #


# @cli.command()
# def test(
#     departement: int = typer.Option(74, '-d', '--departement'),
#     instance_number: int = typer.Option(7, '-i', '--instance'),
#     instance_limit: int = typer.Option(0, '-l', '--limit'),
#     cities: list = typer.Option(["La Roche-sur-Foron"], '-c', '--cities')
# ):
#     instance_limit = math.trunc(get_departement_size(departement)/instance_number)+1 if not instance_limit else instance_limit
#     instance = list(range(0, instance_number * instance_limit, instance_limit))

#     if instance_limit > 50:
#         confirmation = typer.confirm(f"""Each instance will contain more than 50 city,
# we recommand not to do that, and increase the instance number. The odoo may not be able to go trough.
# Would you like to continue with you're '{instance_limit}' ?""")

#         if not confirmation:
#             raise typer.Abort()

#     print(instance_limit, instance, departement, instance_number, cities)


@cli.callback()
def callback():
    """
    MyCityCo2 data processing script
    """

    # TODO: Add log level parameters and call it here
