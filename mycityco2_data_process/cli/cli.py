import fnmatch
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
                # dataset=["Amancy"],
                # dataset=["Fontès"],
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

            logger_config.send_discord(
                f"The '{departement}' has been imported and exported"
            )
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
    _path = const.settings.TMP_DATA
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
                file_src_path = const.settings.TMP_DATA / file
                if file != f"{name}.csv":
                    file_dst_path = dst_path / file
                    os.rename(file_src_path, file_dst_path)
                else:
                    file_data_path = const.settings.DATA_PATH / file
                    os.rename(file_src_path, file_data_path)

        logger.info(f"All files moved to '{dst_path}'")


@cli.command()
def cleaner(
    dev: bool = typer.Option(False, "-d", "--dev"),
    step1: bool = typer.Option(True, "-1", "--no-step1"),
    step2: bool = typer.Option(True, "-2", "--no-step2"),
    step3: bool = typer.Option(True, "-3", "--no-step3"),
    step4: bool = typer.Option(True, "-4", "--no-step4"),
    step5: bool = typer.Option(True, "-5", "--no-step5"),
    delete: bool = typer.Option(False, "--delete"),
    no_save: bool = typer.Option(False, "-s", "--no-save"),
):
    """
    * Step #1:
    Step 1 is there to check if all required columns are in the CSV, and in the good order. Add -1 to remove step from cleaner.

    * Step #2:
    Step 2 is there to check that no data is NaN, None, etc etc, so we don't have empty line or columns. Add -2 to remove step from cleaner.

    * Step #3:
    Step 3 is used to know if city have account.move for all selected year. Add -3 to remove step from cleaner.

    * Step #4:
    Step 4 delete all the account.move that are in the account placeholder. Add -4 to remove step from cleaner.

    * Step #5:
    Step 5 only keep the name from the name columns. Remove everything after |. Add -5 to remove step from cleaner.

    * Dev mode:
    Dev mode remove the colomns to delete. Automatic disable step 1, 2, 4
    """

    if dev:
        step1 = step2 = step4 = False

    PATH = const.settings.DATA_PATH

    REQUIRED_COLUMNS = [
        "city_id",
        "city_name",
        "account_code",
        "account_name",
        # "account",
        "journal_code",
        "journal_name",
        "entry_year",
        "entry_amount",
        "entry_currency",
        "entry_carbon_kgco2e",
        # "emission_factor_name",
        "postal",
        "category_code",
        "category_name",
    ]

    DROP_COLUMNS = [
        "line_label",
        "label",
        "account",
        "emission_factor_name",
    ]

    ERROR_FILE = []

    WARNING_YEAR = list(range(2016, 2022))  # const.settings.YEAR

    sorted_file = sorted([f.name for f in os.scandir(const.settings.DATA_PATH)])

    step5_city_global = []

    def _retreive_only_name(vals):
        if "|" in vals:
            return vals.split("|")[0]
        return vals

    for filename in sorted_file:
        if not fnmatch.fnmatch(filename, "*.csv"):
            continue
        logger.success(f"{filename} - Reading CSV")

        csv_path = (PATH / filename).as_posix()

        csv_file = pandas.read_csv(csv_path)

        file_error_count = 0

        if not dev:
            # Pre Step #1
            for col in DROP_COLUMNS:
                if col in csv_file.columns:
                    csv_file = csv_file.drop(columns=[col])

        # Step 1
        if step1:
            if csv_file.columns.to_list() == REQUIRED_COLUMNS:
                logger.info(f"{filename} - STEP 1: OK")

            else:
                logger.error(f"{filename} - STEP 1: NOT OK")
                file_error_count = +1
                differencies = list(
                    set(csv_file.columns.to_list()) - set(REQUIRED_COLUMNS)
                )
                if differencies:
                    logger.error(
                        f"{filename} - Colums '{', '.join(differencies)}' shall not be there"
                    )
                else:
                    logger.error(f"{filename} - Missing columns")
                    continue
        # Step 1

        # Step 2
        if step2:
            if len(csv_file[csv_file.isna().any(axis=1)]):
                logger.error(f"{filename} - STEP 2: NOT OK")
                continue
            logger.info(f"{filename} - STEP 2: OK")
        # Step 2

        # Step 3
        if step3:
            step5_city = []

            city_name = csv_file["city_name"].apply(_retreive_only_name).unique()

            for name in city_name:
                city_df = csv_file[
                    csv_file["city_name"].apply(_retreive_only_name) == name
                ]

                years = [int(year) for year in city_df["entry_year"].unique()]

                for year in WARNING_YEAR:
                    if year not in years:
                        step5_city.append(f"{name}|-|{year}")
                        logger.debug(
                            f"{filename} - The City '{name}' don't have any account.move for '{year}'"
                        )

            if step5_city:
                step5_city_global += step5_city
                logger.warning(f"{filename} - STEP 3: NOT OK (WARNING)")
            else:
                logger.info(f"{filename} - STEP 3: OK")
        # Step 3

        # Step 4
        if step4:
            csv_file = csv_file.drop(csv_file[csv_file["account_code"] == 0].index)
        # Step 4

        # Step 5
        if step5:
            csv_file["city_name"] = csv_file["city_name"].apply(_retreive_only_name)
        # Step 5

        if file_error_count >= 1:
            logger.error(f"File '{filename}' has {file_error_count} errors")
            ERROR_FILE.append(filename)
        else:
            if not no_save:
                csv_file.to_csv(const.settings.CLEANED_PATH / filename, index=False)

    for data in step5_city_global:
        if ERROR_FILE:
            break

        name, year = data.split("|-|")

        logger.warning(f"The City '{name}' don't have any account.move for '{year}'")

    for file in ERROR_FILE:
        logger.error(f"File '{file}' has errors")

    if delete:
        logger.sucess("")
        os.remove(csv_path)


@cli.callback()
def callback(
    log_level: const.LogLevels = typer.Option("debug", "--level", help="Set log level"),
):
    """
    MyCityCo2 data processing script
    """

    logger_config.setup(str(log_level).upper())
