This site contains the project documentation for the
`mycityco2_data_process` project.

## Table Of Contents

The documentation follows the best practice for
project documentation as described by Daniele Procida
in the [Diátaxis documentation framework](https://diataxis.fr/)
and consists of four separate parts:

1. [Tutorials](tutorials.md)
2. [How-To Guides](how-to-guides.md)
3. [Reference](reference.md)
4. [Explanation](explanation.md)

Quickly find what you're looking for depending on
your use case by looking at the different pages.

## Project Overview

MyCityCO2 Data Processing is a Python package designed to facilitate the import and export of municipality data from a country into Odoo, a popular Enterprise Resource Planning (ERP) system. This package provides functionality to import data from municipalities, perform data processing tasks, and export the processed data to CSV format.

## Features

- Import data from various municipalities.
- Process and analyze the imported data.
- Export the processed data to CSV format.
- Command-line for easy interaction.
- Integration with Odoo ERP system.

## Prerequisites

- Python > 3.8
- Access to an Odoo system (not optional)

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/MyCityCO2/mycityco2-data-processing.git
```

2. Navigate to the project directory:

```bash
cd mycityco2-data-processing
```

3. Run using poetry in dev mode:

```bash
poetry run mycityco2 run fr --departement=74
```

Or Install directly the package:

```bash
pip install mycityco2-data-process
```

## Usage

MyCityCO2 Data Processing is designed to be run as a Command-Line Interface (CLI) application using the Typer module.

To run the project, use the following command:

```bash
mycityco2 run <importer> --departement <departement>
```

For example:

```bash
mycityco2 run fr --departement 74
```

You can also use `--help` to get an overview of the project:

```bash
mycityco2 --help
```

## Contributing

Contributions to MyCityCO2 Data Processing are welcomed. To add new features or fix bugs, please follow these steps:

- Fork the mycityco2-data-processing repository on GitHub.
- Create a new branch for your feature or bugfix: `git checkout -b my-new-feature-or-fix`.
- Add your code and tests for the new feature or fix.
- Commit your changes: `git commit -m 'Add my new feature or fix'`.
- Push your changes to your forked repository: `git push origin my-new-feature-or-fix`.
- Open a pull request to merge your changes into the main branch.
- The maintainers will review your contribution as soon as possible!

## License

This project is licensed under the GNU Affero General Public License v3.0. Please refer to the LICENSE file for more information.

## Contact

For any inquiries, feedback, or issues, please contact:

- Adam Bonnet (contact@mycityco2.org)
- Remy Zulauff (contact@mycityco2.org)
