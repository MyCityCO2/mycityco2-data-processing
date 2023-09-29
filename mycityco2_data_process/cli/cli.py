import functools
import math
import os
import time

import pandas
import typer
from loguru import logger
from multiprocess.pool import Pool

from mycityco2_data_process import const
from mycityco2_data_process import logger as logger_config
from mycityco2_data_process import runner
from mycityco2_data_process.importer.fr import get_departement_size

cli = typer.Typer(no_args_is_help=True)


@cli.command()
def run(
    departement: str = typer.Option(
        "74",
        "-d",
        "--departement",
        help="What departement do want to retreive",  # 74 as default value
    ),
    instance_number: int = typer.Option(
        7,
        "-p",
        "--process",
        help="How many instance do you want to create (speed up the process)",
    ),
    instance_limit: int = typer.Option(
        0, "-l", "--limit", help="How many city per instance"
    ),
    force: bool = typer.Option(False, "-f", "--force", help="Remove warning error"),
    no_delete_db: bool = typer.Option(
        False, "-nd", "--no-delete-db", help="Skip the part where it delete the db"
    ),
    importer: const.ImporterList = typer.Argument(help="What importer you want to use"),
):
    const.settings.NO_DELETE_DB = no_delete_db
    start_time = time.perf_counter()
    match importer.name:
        case "france":
            departement_size = get_departement_size(departement)

            if not departement_size:
                logger.error(f"The '{departement}' departement seem to not exist")
                raise typer.Abort()

            instance_limit = (
                math.trunc(departement_size / instance_number) + 1
                if not instance_limit
                else instance_limit
            )
            instance = list(range(0, instance_number * instance_limit, instance_limit))

            if not force:
                if instance_limit > 50:
                    confirmation = typer.confirm(
                        f"""Each instance will contain more than 50 city,
        we recommand not to do that, and increase the instance number. The odoo may not be able to go trough.
        Would you like to continue with you're '{instance_limit}' ?"""
                    )

                    if not confirmation:
                        raise typer.Abort()

            func = functools.partial(
                runner.init,
                # dataset=["Viols-le-Fort","Saint-Vincent-de-Barbeyrargues","Sainte-Croix-de-Quintillargues","Salasc","Saturargues","Saussan","Saussines","Sauteyrargues","Sauvian","Sérignan","Servian","Sète","Siran","Sorbs","Soubès","Soumont","Sussargues","Taussac-la-Billière","Teyran","Thézan-lès-Béziers","Tourbes","Tressan","Usclas-d'Hérault","Usclas-du-Bosc","Vacquières","Vailhan","Vailhauquès","Valergues","Valflaunès","Valmascle","Valras-Plage","Valros","Vélieux","Vendargues","Vendémian","Vendres","Verreries-de-Moussans","Vias","Vic-la-Gardiole","Vieussan","Villemagne-l'Argentière","Villeneuve-lès-Béziers","Villeneuve-lès-Maguelone","Villeneuvette","Villespassans","Villetelle","Villeveyrac","Viols-en-Laval", "Montpellier"],
                # dataset=["Aigrefeuille-sur-Maine", "Villemagne-l'Argentière"],
                dataset=[],
                instance=instance,
                instance_number=instance_number,
                instance_limit=instance_limit,
                departement=departement,
            )
            logger_config.send_discord(
                f"Starting import of the '{departement}' departement"
            )
            try:
                with Pool(instance_number) as p:
                    p.map(func, instance)

            except KeyboardInterrupt:
                logger.info("Ctrl-c entered. Exiting")

            # logger_config.send_discord(
            #     f"The '{departement}' has been imported and exported"
            # )
        case _:
            logger.error("This importer doesn't exist")
            raise typer.Abort()

    end_time = time.perf_counter()

    final_time = end_time - start_time

    logger.success(
        f"All took {final_time} secondes / {final_time / 60} minutes to execute"
    )


@cli.command()
def csv(
    merge: bool = typer.Option(False, "-m", "--merge"),
    delete: bool = typer.Option(False, "-d", "--delete"),
    name: str = typer.Option("city_data", "-n", "--name"),
    move: bool = typer.Option(False, "--move"),
):
    _path = const.settings.TEMP_FILE_PATH
    if merge:
        # Merging csv #
        logger.info("Merging CSV")

        dataframe = pandas.DataFrame()

        csv_files = os.listdir(_path.resolve().as_posix())
        for file in csv_files:
            if file.endswith(".csv"):  # and file.startswith("temp")
                logger.info(f"Merging '{file}'")
                path = _path / file
                csvfile = pandas.read_csv(path.as_posix())
                dataframe = pandas.concat([dataframe, csvfile], ignore_index=True)

                if delete:
                    os.remove(path)

        dataframe.to_csv(f"{_path.as_posix()}/{name}.csv", index=False)

        logger.info("CSV Merged")
        # Merging csv #

    if move:
        logger.info("Starting moving the files")
        files = os.listdir(_path.resolve().as_posix())
        dst_path = const.settings.ARCHIVE_PATH / name

        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
        for file in files:
            if file.endswith(".csv"):
                logger.info(f"Moving file '{file}'...")
                file_src_path = const.settings.TEMP_FILE_PATH / file
                if file != f"{name}.csv":
                    file_dst_path = dst_path / file
                    os.rename(file_src_path, file_dst_path)
                else:
                    file_data_path = const.settings.DATA_PATH / file
                    os.rename(file_src_path, file_data_path)

        logger.info(f"All files moved to '{dst_path}'")


@cli.callback()
def callback(
    log_level: const.LogLevels = typer.Option("debug", "--level", help="Set log level"),
):
    """
    MyCityCo2 data processing script
    """

    logger_config.setup(str(log_level).upper())
