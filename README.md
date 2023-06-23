![GitHub CI](https://github.com/mycityco2/mycityco2-data-processing/actions/workflows/ci.yaml/badge.svg)
[![License](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](LICENSE)

# MyCityCO2 Data Processing


## Description
MyCityCO2 Data Processing is a Python package designed to facilitate the import and export of municipality data from a country into Odoo, a popular enterprise resource planning (ERP) system. This package provides functionality to import data from municipalities, perform data processing tasks, and export the processed data to CSV format.

## Installation
Make sure you have Python 3.x installed on your system. Clone this repository and run the following command to install the required dependencies:

Usage
To install the MyCityCO2 Data Processing package, use the following command:

```shell
$ pip install mycityco2-data-process
```

## Running the Project
The MyCityCO2 Data Processing package is designed to be run as a command-line interface (CLI) application using the Typer module. Here are the steps to run the project:

```shell
$ mycityco2 run <importer> --departement <departement>
```

per example
```shell
$ mycityco2 run fr --departement 74
```

You can also do --help to get better view of the project.


## Contribution
We welcome contributions to MyCityCO2 Data Processing. To add new features, please follow these steps:

- Fork the mycityco2-data-processing repository on GitHub.
- Create a new branch for your feature: `git checkout -b my-new-feature`.
- Add your code and tests for the new feature.
- Commit your changes: `git commit -m 'Add my new feature'`.
- Push your changes to your forked repository: `git push origin my-new-feature`.
- Open a pull request to merge your changes into the main branch.
- We will review your contribution as soon as possible!

## License
This project is licensed under the GNU Affero General Public License v3.0. Please refer to the LICENSE file for more information.

## Contact
For any inquiries or feedback, please contact:

Adam Bonnet (abo@open-net.ch)  
Remy Zulauff (rzu@open-net.ch)
