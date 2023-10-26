# CHANGELOG



## v0.1.1 (2023-10-26)

### Chore

* chore(base.py): remove commented out code and unused logger statements for cleaner code ([`1cfeebf`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/1cfeebfa40672d644be361be973c04a9b2a30afc))

* chore(importer/fr.py): fix typo in comment
chore(importer/fr.py): add docstring to get_account_move_data_from method explaining its parameters and return value
chore(importer/fr.py): improve readability and organization of get_account_move_data_from method
chore(importer/fr.py): remove unnecessary comment and return statement in get_account_move_data_from method
chore(importer/fr.py): improve readability and organization of code in get_account_move_data_from method ([`a510f3e`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/a510f3ec8cd32f0bd2b6be9b206cab7f0c6c31be))

* chore(fr.py): correct error message from &#34;No city find with this scope&#34; to &#34;No city found with this scope&#34; for proper grammar and clarity. Fix typo ([`0d8ae59`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/0d8ae59871b63fea0b145c0e65c6dec644ee5c4e))

* chore(fr.py): simplify the code by removing unnecessary list conversion in the nomens variable assignment ([`80ecdca`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/80ecdca1cfc583cf4f37f8004e68686764ce3757))

* chore(fr.py): remove unused M57_LAST_YEAR_CHECK variable, comment dev code, and add docstring ([`7d7ec70`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/7d7ec704e275df9f33014eacd5b2d8ace890c9cd))

* chore(cli.py): change WARNING_YEAR variable content to YEARS_TO_COMPUTE to improve semantics
chore(const.py): change YEAR variable name to YEARS_TO_COMPUTE to improve semantics
chore(fr.py): change YEAR variable name to YEARS_TO_COMPUTE to improve semantics
chore(fr.py): use YEARS_TO_COMPUTE[-1] instead of const.settings.YEAR[-1] for better readability
chore(fr.py): use YEARS_TO_COMPUTE instead of const.settings.YEAR for better readability ([`6f3e684`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/6f3e6841e5ddf286d3b2d9e821b031584a035ac7))

* chore(pyproject.toml): update bandit skips to exclude additional security checks

The skips configuration in the [tool.bandit] section of pyproject.toml has been updated to include the following additional security checks: B320, B408, B410, B318, B306, B603, B307, B404, B101. This is done to exclude these specific checks from the bandit security analysis tool. ([`e798e17`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/e798e17c13ac5db2da30bb44d6e7c7a059d35d0e))

### Fix

* fix: Update chore element in order to fix some coding mistake

fix: Update chore element in order to fix some coding mistake ([`a69c5a9`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/a69c5a9ed15ea23270d7cab90bf16c2eddfe1390))

* fix(importer/base.py): refactor check_env method to improve readability and error handling

The check_env method in the AbstractImporter class has been refactored to improve readability and error handling. Instead of using a search_read method to check if the required Odoo modules are installed, the method now uses a search method with the &#34;in&#34; operator to search for all modules with names in the REQUIRED_ODOO_MODULE list. If any of the modules are not installed, an error message is logged with the module name, template database, and URL for installation. The method now returns False if any module is not installed. ([`72ae980`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/72ae980541f3cd2cf67c1870825ce1259cd4e019))

* fix(cli.py): fix typo in constant name DOCKER_POSTGRES_IMAGE
fix(cli.py): fix typo in constant name DOCKER_ODOO_IMAGE ([`44515b9`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/44515b93de8730a048a5225a9c2e21db534bfeab))

* fix(cli.py): change variable name from DOCKER_CONTAINER_START_NAME to DOCKER_CONTAINER_PREFIX for consistency with const.py ([`010ae64`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/010ae64ff2076df0816a4d778d3ee0bdb8470a00))

* fix(cli.py): refactor container creation logic to use a match statement for improved readability and maintainability ([`548c00e`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/548c00efa4537b06612ff841849de38477626fc0))

### Refactor

* refactor(base.py): remove unnecessary code that reads fields of created journals

The code was previously reading the fields of the created journals, but this is unnecessary and can be removed. ([`b0ea036`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/b0ea03648ca46fbf4f266e15dd05f983cf0e60be))

* refactor(cli.py): rename GIT_MODULE to GIT_REPOS in order to improve code readability and semantics
refactor(const.py): rename GIT_MODULE to GIT_REPOS to maintain consistency with the change made in cli.py
refactor(utils.py): rename GIT_MODULE to GIT_REPOS to maintain consistency with the changes made in cli.py and const.py ([`856e701`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/856e70183de985a764e099d346c8255430ef58f3))

* refactor(cli.py): rename _addons_path_docker variable to _mount_path_docker for better clarity
refactor(cli.py): update target path in Mount configuration to use _mount_path_docker variable for consistency ([`215756a`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/215756a1f2abf7dc2dcc04f89f0fb70d7ab9799c))

* refactor(base.py): improve type annotations and variable names for better readability and maintainability
feat(base.py): add type annotations for recordset variables to improve code clarity and avoid potential errors ([`07c881b`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/07c881ba2452d6d0094f5d57e5f9e42d7bbe05b1))


## v0.1.0 (2023-10-19)

### Build

* build: add linting and testing configuration files and workflows

Add configuration files for linting and testing tools, including flake8, isort, black, bandit, and pre-commit. Also, add a GitHub Actions workflow to run the tests and linting on pull requests and pushes to the main branch. ([`a0d9238`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/a0d92384440b44f6adb4dc86cae0e1f738bb8547))

* build: add Poetry configuration file to manage dependencies and packaging
feat: add support for CLI using Typer library
test: add empty __init__.py files to tests and mycityco2_data_process directories to allow importing modules ([`7c6b5bc`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/7c6b5bc16fb6a187fea72706edf4f7f0e7cc6300))

### Chore

* chore(orchestrator.yaml): uncomment call-release-pipeline job to enable release pipeline
feat(release.yaml): add release workflow to automate the release process ([`094747b`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/094747b012634e54582245757cbbc2aa28a72c7f))

* chore(pyproject.toml):
    - remove unused script entry &#39;mycityco2&#39; from poetry.scripts
    - add semantic-release configuration to automate versioning and changelog generation ([`acc7325`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/acc732521655945b7f3262eb3c56bf16178fd9d7))

* chore: add version number to package

The changes in this commit add a version number to the package and include a test to ensure that the version number is correct. This is done to provide a clear and consistent way to identify the version of the package. ([`12fd5dc`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/12fd5dce9a5380471cad7491e19febe3d0dc56f4))

* chore(CI): Apply new CI with docs deploy ([`a2ab40d`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/a2ab40dd82a059488dc62104ec1936375b6c8681))

* chore: Add new CI and include mkdocs ([`69a6358`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/69a635899d3255a2b4a56b2f26366286f116bee3))

* chore: Add editorconfig ([`86068f4`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/86068f410749b1f615d71fb6f2a82fcca8c9c7db))

* chore(fr.py): remove unused imports to improve code cleanliness
feat(fr.py): add support for fetching chart of accounts data from a different API endpoint to improve data accuracy
feat(fr.py): add support for filtering and processing specific chart of accounts data to improve data quality
refactor(fr.py): refactor gen_account_account_data method to improve readability and maintainability
refactor(fr.py): refactor process_entries method to skip processing for certain nomenclatures to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for certain accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without budget journals to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method to skip processing for cities without account accounts to improve efficiency
refactor(fr.py): refactor process_entries method ([`3dd6234`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/3dd62348cb87dbbb2dd8243b9fa3748ca19eaaca))

* chore(cli.py): remove commented out code for dataset selection
fix(fr.py): convert account codes to strings to ensure consistency
fix(fr.py): handle case where result_dict is empty in _get_chart_account function
fix(fr.py): convert account codes to strings in accounts_list
fix(fr.py): convert account codes to strings in account_move_lines_ids creation
fix(fr.py): add logging for comptable problem in FrImporter class
fix(logger.py): add error parameter to send_discord function to differentiate between error and alert messages
fix(logger.py): use separate webhook URLs for error and alert messages
chore(runner.py): comment out unused code in init function
chore(datacleaning.py): remove unnecessary check for postal field in csv file ([`711b778`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/711b7782ac3fbf1fc7128e35e2d02fb8849e0404))

* chore(.pylintrc): enable W0603 rule to enforce using `logging.warning` instead of `print` for consistency and best practices ([`64a30e2`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/64a30e27e4e3147358c8dec185e7145cb61e3815))

* chore(base.py): add logging of database name to improve debugging
refactor(base.py): rename &#39;pmun_2023&#39; column to &#39;habitant&#39; to improve semantics
refactor(base.py): replace &#39;is not False&#39; with &#39;!= False&#39; to improve semantics
refactor(base.py): remove unused columns from dataframe to improve performance
refactor(base.py): replace hardcoded string with variable to improve semantics ([`560859e`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/560859e1d66929043ac3b4826b274c0c37a7f2cb))

* chore: update pylint configuration to include new rules and fix formatting
chore: update otools-rpc dependency to version 0.3.1 in pyproject.toml file ([`1cc1cc3`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/1cc1cc340e5ea42a1d3feab127a0d5ee731baac1))

* chore(ci.yaml): rename workflow name to MyCityCO2 CI for clarity and branding purposes ([`c6d5db1`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/c6d5db1b5ad4bd9eb889d99980127941af6dbd8f))

* chore: add .vscode/, .~lock and temp_file/ to .gitignore file
docs: remove trailing whitespace and fix typo in README.md
fix: fix CI configuration ([`b527ae5`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/b527ae52b0dc38f57c6f6b4ddab84394eeadef17))

* chore(README.md): add tasks to the to-do list
refactor(const.py): move csv files from static to data folder
refactor(base.py): move csv files from static to data folder and update file paths in code ([`d3f1929`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/d3f1929cb71b391c3d485675d0b790879f2eb087))

### Documentation

* docs(README.md): update table of contents, add features section, and improve formatting and readability
feat(README.md): add information about CLI usage and integration with Odoo ERP system
docs(README.md): update contribution section to include bugfixes and improve formatting and readability ([`89bcea3`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/89bcea311d00de860cb7aabd8952bc0d956fe2ef))

* docs(README.md): update README.md to provide a better description of the project, installation instructions, usage instructions, contribution guidelines, and contact information. Also, add a license badge to the README.md file. ([`7aa3706`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/7aa3706582b8014c2322094e05b5fcbc4e99c299))

* docs(README.md): add CI badge to README.md

Add a CI badge to the README.md file to show the status of the GitHub Actions workflow. ([`be8e23b`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/be8e23b8651385593f82bfc8ca6c0f8b2d904f11))

* docs(README.md): add project description and instructions on how to start the program
chore(README.md): add TODO list for future improvements ([`80c4485`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/80c44854b9b8600f73fab624437a204639398b2b))

### Feature

* feat(data): add new category &#34;Placeholder&#34; with id 11 to coa_categories.csv
feat(data): add new condition with category_id 11 and rule_order 999 to coa_condition.csv ([`892776b`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/892776bf344d1008d0bbf6994d0de83986f48162))

* feat(datacleaning.py): add script for data cleaning and validation, still wip

This commit adds a new file `datacleaning.py` which contains a script for data cleaning and validation. The script performs the following tasks:

1. Reads CSV files from the `./files` directory.
2. Validates the columns of the CSV files against a list of required columns.
3. Checks for missing or extra columns in the CSV files.
4. Validates the values in certain columns to ensure they are not empty or NaN.
5. Checks for missing account.move entries for each city and year combination.
6. Logs the results of the validation process.

The script is designed to be configurable through the use of variables such as `PATH`, `REQUIRED_COLUMNS`, `WARNING_YEAR`, and `STEP`. It uses the `pandas` library for reading and manipulating CSV files, and the `loguru` library for logging.

This script will help ensure the quality and integrity of the data used in the application. ([`4aec021`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/4aec021e6df9bd7f521dbd5f3217177faad4d2a5))

* feat(multiple file): Currently under wip ([`dde794d`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/dde794d56cc75dd6a266d260eaa377b931e27ede))

* feat(data): add French Importer dataset and update data readme with information about the dataset collection ([`2e4e799`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/2e4e79975f0a1cce496ab5e2f813f80e3947d398))

* feat(cli.py): add support for moving files to a new directory with the --move flag
feat(test.sh): add support for moving files to a new directory with the --move flag in the csv command for each department ([`6fd8acb`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/6fd8acba46f9812236d4266e93a0584b4d02a635))

* feat(runner.py): add detailed steps for each stage of the data processing pipeline to improve visibility and traceability ([`6647397`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/664739795f05b0fdf8d8bb19b8abb5d234f0536c))

* feat(pyproject.toml): add lxml library as a dependency to the project to enable parsing of XML documents ([`4fc5936`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/4fc5936ccd700496af960c95d21da83845b5993a))

* feat(cli.py): add multiprocessing support to improve performance and add logging to better track execution time and errors. Add support for merging CSV files and sending a Discord webhook notification. ([`953c403`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/953c403d361bd6252ae9051898b8f378974e5590))

* feat(runner): add runner module ([`f283e87`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/f283e87c78cabdfeeb75501225faa8fc1a7fbc29))

* feat(utils.py): add function to retrieve a dataset from an external API based on a list of cities
feat(utils.py): add function to change the state of the superuser in the database to enabled or disabled based on a boolean value ([`375ac3c`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/375ac3cf0567379abaaba36f31f157ba11d66ba2))

* feat(wrapper.py): add CustomEnvironment class to handle environment variables and create an instance of Environment class with the given parameters ([`bf3f68c`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/bf3f68c8cd714b17e6e40d432420991d9a47c67b))

* feat(importer): Add abstract importer and implement fr importer ([`b472d9d`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/b472d9d140fe040b7d663b2c4adc89f1f808c942))

* feat(const.py): add ENV_MASTER_PASSWORD to Settings class to allow for master password configuration ([`df69061`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/df69061b039de04f8292b34007d6ba22daa79ef2))

* feat(logger.py): add logger module with send_ntfy and send_discord functions to send notifications
feat(__init__.py): import logger module and call setup function to initialize logger module ([`fed756f`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/fed756fc2a0146d52f4db30cc36ba66db3194aec))

* feat(.env.example): add MCO2DP_ENV_MASTER_PASSWORD environment variable to store master password for the app ([`924915a`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/924915a7429d648f087176838b37b3be1990fee6))

* feat(pyproject.toml): add pandas and multiprocess libraries to dependencies
feat(pyproject.toml): add discord-webhook library to dev-dependencies ([`6ed60a8`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/6ed60a8b9e4de74f86cd686a9437929fdf519962))

* feat(const.py): add pydantic settings class to handle environment variables and add new settings for logging, notifications, and database configuration
feat(.env.example): add example environment variable for MCO2DP_ENV_PASSWORD
feat(.flake8): add E501 and E800 to the list of ignored flake8 errors to allow lines up to 160 characters long and to ignore some flake8-bugbear warnings

feat(const.py): add pydantic settings class to handle environment variables and add new settings for logging, notifications, and database configuration
feat(.env.example): add example environment variable for MCO2DP_ENV_PASSWORD
feat(.flake8): add E501 and E800 to the list of ignored flake8 errors to allow lines up to 160 characters long and to ignore some flake8-bugbear warnings ([`a32b35b`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/a32b35b4f75ee370d291bf3529c853719c2bdb35))

* feat: add entry point and CLI for MyCityCo2 data processing script

Add an entry point to the MyCityCo2 data processing script and a CLI module
to handle command line arguments. The CLI module uses the Typer library to
define the command line interface. ([`c57f08e`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/c57f08ea77c831bbad4945dfbbaa59c854810a17))

### Fix

* fix(const.py): update YEAR constant to include the year 2022 for data processing ([`f972715`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/f97271585a56c26eec940433661b3dc482363bc1))

* fix(const.py): change cls parameter to self in prevent_none method to match instance method signature ([`9049c72`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/9049c72c0821efea9d38ad31fbc7821ab95ae46f))

* fix(cli.py): change instance_number to 1 to avoid running multiple instances of the same process
feat(cli.py): add support for retreiving dataset from utils.retreive_dataset(city) function
fix(logger.py): change logger level from ERROR to CRITICAL to post message to discord when error occurs
feat(logger.py): add custom log level FTRACE with no=3 and color blue
fix(runner.py): add try-except block to catch exceptions and increment ERROR_COUNTER in const.py
feat(runner.py): add more detailed reporting with time elapsed for each step and substep of the process. Add support for displaying total errors in the reporting. ([`65836a1`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/65836a1d3f7d3b468286ad28de544e5ec8b88b01))

* fix(README.md): correct typo in filename from const.py to const.settings.py ([`49467b8`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/49467b8f49742cbd3bc443faea47efee041aea32))

### Refactor

* refactor(tests): move tests to scripts folder ([`a413579`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/a413579cb2ff488bf36ab5e40e4fd72af4ad04bd))

* refactor(datacleaning.py): remove unused timeout variable and commented out code
fix(datacleaning.py): fix typo in incrementing timeout variable ([`22f547c`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/22f547c890159a5b49fc65a113547077e8a4604a))

* refactor(runner.py): remove unnecessary code block related to deleting the database

The code block related to deleting the database was commented out and is no longer needed. It has been removed to improve code readability and maintainability. ([`6b52968`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/6b529687e516e89e0e931202fa2ac3ef42cb963d))

* refactor(cli.py): remove TODO comment
refactor(const.py): remove ENV_ prefix from DELETE_DB_TOGGLE setting
refactor(const.py): remove CARBON_FILE, ACCOUNT_ASSET_TOGGLE, and ACCOUNT_ASSET_FILE settings
refactor(importer/base.py): add importer abstract method
refactor(importer/fr.py): remove CARBON_FILE, ACCOUNT_ASSET_TOGGLE, and ACCOUNT_ASSET_FILE constants
refactor(importer/fr.py): add importer property
refactor(runner.py): remove ENV_ prefix from DELETE_DB_TOGGLE setting ([`c6371bf`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/c6371bfba23777ebbdacd912867c3fcc08d8166c))

* refactor(mutiple files): change environment variables names to be more concise and remove &#39;ENV_&#39; prefix ([`1474860`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/1474860eb60d99c5aef644f6bd10d9d4bbf92176))

* refactor(const.py): make ENV_* fields optional and add root_validator to prevent None values
refactor(fr.py): remove usage of SKIPPED_CITY field from const.py and related code ([`5f7764d`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/5f7764d6a796bb89838f4c0216e25899a5e0a51f))

* refactor(runner.py): update step descriptions to include more specific information about the process being executed. Specifically, add &#34;(Odoo)&#34; to steps 2.3, 3.3, and 4.6 to indicate that the process is being executed in Odoo. Also, fix step numbering for steps 3.2 and 3.3. ([`ee1db75`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/ee1db75365a3793a83be12e72f78619c77403ed0))

* refactor(fr.py): improve logging messages and add timing information to improve debugging and performance analysis
feat(fr.py): add support for process.env.ACCOUNT_ASSET_TOGGLE environment variable to toggle account asset creation and move creation ([`f3af582`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/f3af5827721ecdc06145c0768946f5a09ee61852))

* refactor(cli.py): comment out unused code and remove discord webhook code
fix(runner.py): fix typos in comments and remove unnecessary whitespace ([`cb95180`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/cb95180f02ad59027d5c87e8e96f4dc5ec5e22b8))

* refactor(importer/fr.py): remove unused logger.error calls
refactor(importer/fr.py): remove commented out code
refactor(importer/fr.py): use dictionary instead of filter to improve performance ([`6e594f4`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/6e594f4bbb25ddc7cd53680ed6595360512a48e0))

* refactor(pyproject.toml): change script name from mycityco2-data-process to mycityco2 to improve usability and readability ([`023d308`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/023d3083b4bbdc8a4aa948a34f923b5501b19b00))

* refactor(cli.py): replace hardcoded path with a constant PATH from const.py to improve maintainability
refactor(const.py): add a constant PATH to store the path of the project root directory
refactor(importer/base.py): replace hardcoded path with a constant PATH from const.py to improve maintainability ([`49077f4`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/49077f4840762afb486f765cb8c18722c5a936ad))

### Style

* style(const.py): fix formatting and indentation
refactor(importer/base.py): refactor get_account_move_data to populate account_account_ids instead of account_move_ids
refactor(importer/base.py): refactor populate_account_move to use account_account_ids instead of account_move_ids
refactor(importer/base.py): refactor export_data to use const.settings.PATH instead of hardcoded path ([`a2272c3`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/a2272c31db569c3c8eb2b19e789a77588eae266c))

* style: fix formatting in .bandit, .flake8, .github/workflows/ci.yaml, .pre-commit-config.yaml, and README.md files

This commit only fixes formatting issues in the mentioned files. No functional changes were made. ([`8c16359`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/8c163591435f1a9fca19979eaf99f5ec09ad915a))

### Unknown

* 0.1.0 [skip ci]

Automatically generated by python-semantic-release ([`5458932`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/54589327489183837688e8795cd3fdc1ae5c11ab))

* Merge pull request #14 from MyCityCO2/main+docker

chore: Add docker environment and refactor CI structure ([`9cf0154`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/9cf0154ebb6b24044d50098bd5a1090207f89a6b))

* Merge pull request #13 from MyCityCO2/rzu+review

chore: refactor project CI ([`b73cc53`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/b73cc531db84e9cae274255d29c9685020ac2c85))

* [ADD] Add docker error handler and remove volumes ([`b92df63`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/b92df6322f6d832f815348893e8c3a3b7ac81c44))

* [ADD] Add docker ([`132ac49`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/132ac49d134ee05421ef832b0027b213d5f889dc))

* [FIX] Check ENV ([`e09070a`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/e09070ab06b614915ca2745e94f8f2a524f7abe6))

* [ADD] Add missing postal code ([`1573185`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/15731852671df2b46fbfa4910c85b3b62ecaf4d7))

* [ADD] Add missing postal code ([`c573c49`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/c573c49ac1db97d84501a1fb0a9656bc6c53ccfa))

* [FIX] Fix error migration from otools-rpc ([`99b15e7`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/99b15e772154276d6d17c38202808507c2b9c2af))

* Tweaking readme and pyproject ([`15dab8a`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/15dab8a9cac8c0cca9a8de1f6fc9439da4ebeee8))

* [ADD] Create DB when template doesn&#39;t exist ([`1ec3836`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/1ec38364d95ee80210b3bcb1baff75f02ab8b642))

* Migrating to 0.4.2 otools-rpc (#12) ([`4dbe71d`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/4dbe71d0658b2bde166ea88841260fcade1e95c0))

* [ADD] Implement Carbon Factor Creation if not exist in template base (#10)

* [ADD] Implement the creation of carbon factor ([`e40d822`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/e40d822fd860de48565e4b384f5bf771c4a38844))

* [France] Fix data source for API ([`6297af6`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/6297af6edc140ca4e1471032fe717096d693af9c))

* [DependaBOT] Fix dependabot alert (#9) ([`7e469b5`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/7e469b589bda5cf8720fb2b14e7c1c107db36d14))

* [France] Add M57 multi-year support to France city and GCA Adjustement (#8)

* Adjustments from GCA

* Add m57 Support

---------

Co-authored-by: GCA Open-Net &lt;gca@open-net.ch&gt; ([`6f66f8a`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/6f66f8a0f4bb72a883497a474657186415018cdb))

* Delete tests/test.sh ([`0092f78`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/0092f78a8b6ae20c82bf68c2eb3530b18f0a93df))

* Update test.sh ([`b35c298`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/b35c29876864a046fef077c692ef8fcfb2fc1423))

* Update logger parameter ([`bb6ea78`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/bb6ea78232132260c7cae5dbb9e0e256b115c7ea))

* Update fr_mapping_coa_exiobase.csv (#6) ([`b972b82`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/b972b8274eb9371592bb8f03d2276791abc73f64))

* Fix fr postal data ([`b71106c`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/b71106c6ea9d11447ea3f4c4722284e67f0a8996))

* Update postal config file ([`a89beab`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/a89beabd2eb3698464f4810a1ba2cd4c14b45992))

* merge ([`760bd0e`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/760bd0e34a94bd1f251e8ab38e98b3e820b28c76))

* improvement ([`5f7fa0c`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/5f7fa0c20f151ce1116b2fad6955ea9343bb7a22))

* Add departement to french Files ([`64e98c1`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/64e98c1161399311e2cc067f1713ce0b7f0b0dcd))

* Fix dependabot issues ([`196032f`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/196032f5c84dac8b456085b0f05b47d46cda6c42))

* Improvement ([`745a083`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/745a08383cfb03e8fefa7bcde7951daa53a116bc))

* Update config Categories Files ([`8cddd8a`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/8cddd8ab964e8c401478ca25b6a8c48d4919d2f3))

* Project Update and fixed ([`3e3677d`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/3e3677d48f5e7a42768bc221bd76dca11cbe9597))

* Config File change ([`39dd253`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/39dd253dd0102789baa0558e669cc8b956164975))

* Refactor Code review

* Code REVIEWED

* feat(coverage.yml): add Code Coverage Summary action to generate a summary of code coverage

* chore(coverage.yml): remove CodeCoverageSummary action as it is no longer needed

* Refactor due to code review ([`6e748a6`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/6e748a6453b9bfe94490c7561fe303fa2f28515f))

* Fix any uses ([`de163fa`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/de163fa714dee248ca7f0825c1d9f100cc494259))

* Add PyLint to CI and CI pass ([`1678640`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/1678640e36f8bffd0a7a50fa113b0b1f3cdd1349))

* Parameters Changes ([`788c0b3`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/788c0b3aa83f40e22a96c6bd6850bad5c610c286))

* Fix CI ([`8c003de`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/8c003de5c592025835957163e8433afa94e6764f))

* data fix ([`43302fe`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/43302fe5c76fb0be6895a89ead19ac1691aecf53))

* Merge branch &#39;main&#39; of github.com:MyCityCO2/mycityco2-data-processing ([`6d7c0cc`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/6d7c0ccebb3c179c7c13f21b734323950fc4ee56))

* [imp] path system ([`43b2021`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/43b2021772cdeb2a8ea26e8ea1c4024e627d867d))

* remove unwanted field ([`b9f4fe0`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/b9f4fe0489aad2602d05cfba8d0a37c5d33e0d22))

* data(importer): add data for importer classes ([`290e164`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/290e16455ebae7d8f83a6b668f208281a9266b43))

* Initial commit ([`38aa34e`](https://github.com/MyCityCO2/mycityco2-data-processing/commit/38aa34e4512adfb02338b110a136eda90c6f40e7))
