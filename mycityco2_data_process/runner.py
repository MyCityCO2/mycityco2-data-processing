import time

from loguru import logger
from otools_rpc.db_manager import DBManager

from mycityco2_data_process import const

from . import utils
from .importer.fr import FrImporter
from .logger import send_discord
from .wrapper import CustomEnvironment


def run(
    offset,
    instance_limit,
    env,
    dbname,
    chunksize,
    instance_reste,
    instance_number,
    departement: int = 74,
    dataset: list = [],
):
    start_time = time.time()
    env.authenticate()

    # company = env['res.company'].sudo().search([])

    # logger.warning(env.context)

    if offset == instance_number - 1:
        dataset = dataset[offset * chunksize : (offset + 1) * chunksize]

    else:
        dataset = dataset[
            offset * chunksize : (offset + 1) * chunksize + instance_reste
        ]

    importer = FrImporter(
        limit=instance_limit,
        env=env,
        offset=offset,
        db=dbname,
        departement=departement,
        dataset=dataset,
    )
    # importer = FrImporter(limit=instance_limit, env=env, offset=offset, db=dbname, city_name=["Mégevette", "Onnion", "Saint-Jean-de-Tholome", "Saint-Jeoire", "La Tour", "Ville-en-Sallaz", "Viuz-en-Sallaz", "La Roche-sur-Foron", "Allonzier-la-Caille", "Amancy", "Andilly", "Arbusigny", "Cercier", "Cernex", "La Chapelle-Rambaud", "Copponex", "Cornier", "Cruseilles", "Cuvat", "Etaux", "Menthonnex-en-Bornes", "Monnetier-Mornex", "La Muraz", "Nangy", "Pers-Jussy", "Reignier-Ésery", "Saint-Blaise", "Saint-Laurent", "Saint-Sixt", "Le Sappey", "Scientrier", "Villy-le-Bouveret", "Villy-le-Pelloux", "Vovray-en-Bornes", "Reignier-Ésery", "Arbusigny", "Fillinges", "Monnetier-Mornex", "La Muraz", "Nangy", "Pers-Jussy", "Scientrier", "Cruseilles", "Allonzier-la-Caille", "Andilly", "Cercier", "Cernex", "Copponex", "Menthonnex-en-Bornes", "Le Sappey", "Saint-Blaise", "Villy-le-Bouveret", "Vovray-en-Bornes", "Bonneville", "Arenthon", "Ayse", "Brizon", "Contamine-sur-Arve", "Faucigny", "Fillinges", "Glières-Val-de-Borne", "Marcellaz", "Marignier", "Mégevette", "Onnion", "Peillonnex", "Saint-Jean-de-Tholome", "Saint-Jeoire", "Saint-Pierre-en-Faucigny", "La Tour", "Ville-en-Sallaz", "Viuz-en-Sallaz", "Vougy", "Boëge", "Bogève", "Burdignin", "Habère-Lullin", "Habère-Poche", "Saxel", "Saint-André-de-Boëge", "Villard"])
    # importer = FrImporter(limit=instance_limit, env=env, offset=offset, db=dbname, city_name=["La Roche-sur-Foron"])
    # importer = FrImporter(limit=instance_limit, env=env, offset=offset, db=dbname)

    # only_export = True
    only_export = False

    step1_elapsed_time = (
        step2_elapsed_time
    ) = step3_elapsed_time = step4_elapsed_time = 0

    try:
        step1_start_time = time.perf_counter()
        if not only_export:
            importer.populate_cities()
            importer.populate_journal()
        step1_end_time = time.perf_counter()
        step1_elapsed_time = step1_end_time - step1_start_time

        step2_start_time = time.perf_counter()
        if not only_export:
            importer.populate_account_account()
        step2_end_time = time.perf_counter()
        step2_elapsed_time = step2_end_time - step2_start_time

        step3_start_time = time.perf_counter()
        if not only_export:
            importer.populate_account_move()
        step3_end_time = time.perf_counter()
        step3_elapsed_time = step3_end_time - step3_start_time

        step4_start_time = time.perf_counter()
        if not only_export:
            importer.account_asset_create_categories()
            importer.populate_account_asset()
            importer.account_asset_create_move()
        step4_end_time = time.perf_counter()
        step4_elapsed_time = step4_end_time - step4_start_time
    except Exception:
        const.settings.ERROR_COUNTER += 1
        utils.change_superuser_state(dbname, False)

    # importer.gen_carbon_factor()

    # logger.error(importer.carbon_factor_id)

    end_time = time.time()

    elapsed_time = end_time - start_time

    logger.warning(
        f"Took {elapsed_time} secondes / {elapsed_time / 60} minutes. All data has been send to {dbname}"
    )

    step5_start_time = time.perf_counter()
    logger.info(f"Exporting DATA from {dbname}")
    importer.export_data()
    step5_end_time = time.perf_counter()
    step5_elapsed_time = step5_end_time - step5_start_time
    # logger.critical(f'Export des donnees: {step5_elapsed_time} secondes / {step5_elapsed_time / 60} minutes')

    # Reporting
    total_elapsed_time = (
        step1_elapsed_time
        + step2_elapsed_time
        + step3_elapsed_time
        + step4_elapsed_time
        + step5_elapsed_time
    )

    def _get_formated_text(timer, minute: bool = False):
        seconds = round(timer)
        final_text = f"_{seconds}_ seconde(s)"

        if minute:
            minutes = round(timer / 60)
            final_text += f" / _{minutes}_ minute(s)"

        return final_text

    reporting = f"""
    Chargement de **{importer._city_amount}** villes sur la DB **{importer._db}**
    **Etape 1** - Creation des societes : {_get_formated_text(step1_elapsed_time, minute=True)}
        > **Etape 1.1** - Generation des societes : {_get_formated_text(importer.step1_1, minute=True)}
        > **Etape 1.2** - Creation des societes (Odoo) : {_get_formated_text(importer.step1_2, minute=True)}
    **Etape 2** - Creation des plan comptable : {_get_formated_text(step2_elapsed_time, minute=True)}
        > **Etape 2.1** - Generation des plan comptable : {_get_formated_text(importer.step2_1, minute=True)}
        > **Etape 2.2** - Generation des plan comptable par villes : {_get_formated_text(importer.step2_2, minute=True)}
        > **Etape 2.3** - Creation des plan comptable par villes : {_get_formated_text(importer.step2_3, minute=True)}
    **Etape 3** - Importation comptabilite : {_get_formated_text(step3_elapsed_time, minute=True)}
    **Etape 4** - Creation ammortissement : {_get_formated_text(step4_elapsed_time, minute=True)}
    **Etape 5** - Exporting des donnees et traitement : {_get_formated_text(step5_elapsed_time, minute=True)}

    **Temps total** : {_get_formated_text(total_elapsed_time, minute=True)}

    **Temps approximatif par ville** : {_get_formated_text((total_elapsed_time / importer._city_amount) if importer._city_amount > 0 else total_elapsed_time, minute=True)}
    """

    if const.settings.ERROR_COUNTER > 0:
        reporting += f"""
        __**Total Errors : {const.settings.ERROR_COUNTER}**__
        """

    send_discord(reporting, link=const.settings.ENV_URL + f"/web?db={importer._db}")

    # Reporting


def init(offset, dataset, instance, instance_number, instance_limit, departement):
    pooled = instance.index(offset) + 1

    dbname = (const.settings.ENV_DB + "-" + str(pooled) + "-test").replace(
        "departement", f"{departement}"
    )

    # DBObject
    dbmanager = DBManager(const.settings.ENV_URL, const.settings.ENV_MASTER_PASSWORD)

    dbobject = dbmanager.dbobject

    # logger.error(const.settings.ENV_DB not in dbobject.list())

    if const.settings.ENV_DELETE_DB_TOGGLE:
        dbmanager.drop(dbname)

    if dbname not in dbobject.list():
        dbmanager.duplicate(const.settings.ENV_TEMPLATE_DB, dbname)
    else:
        logger.info(f"DB {dbname} Already exist using this one")
    # DBManagement

    # return
    utils.change_superuser_state(dbname, True)

    env = CustomEnvironment(dbname=dbname).env
    instance_reste = len(dataset) % instance_number
    chunksize = len(dataset) // instance_number

    try:
        # main.run(offset, instance_limit, env.env, dbname, departement=departement)
        run(
            offset,
            instance_limit,
            env.env,
            dbname,
            chunksize,
            instance_reste,
            instance_number,
            departement=departement,
            dataset=dataset,
        )
    except Exception as e:
        utils.change_superuser_state(dbname, False)
        raise Exception(e)

    utils.change_superuser_state(dbname, False)
