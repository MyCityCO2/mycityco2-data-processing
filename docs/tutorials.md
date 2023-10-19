This part of the project documentation focuses on a
**learning-oriented** approach. You'll learn how to
get started with the code in this project.

## Managing an Docker Environment with CLI
### Starting the Docker Environment
Command: start

Description: Use this command in order to create/start an docker environment. You can consider this command as `docker compose up`. When using this command the cli will automaticly create all requirements like the container, volumes, image, etc etc. He will also start them if already created. Only need to run this command ONCE.

```bash
mycityco2 start
```

### Deleting the Docker Environment
Command: stop

Description: Use this command in order to delete an docker environment. When using this command the cli will delete everything that the `start` command created.

```bash
mycityco2 stop
```

## Managing the Importer
### Stating the importer
Command: run

Description: This command is the core of this project. He will duplicate an template DB, and import all the comptability of city(s). This command has multiple arguments that you can use to really scope the process as you need.

Argument:

* Importer (required): This will be the 2 letter code from the country you want to import, in my example I'll use `fr`
* Departement: This will be custom for any country but since I'll use the French Importer I will also use French departement in my example I'll use `74` in my example.
* Process: This option will be the number of process from [multiprocess](https://docs.python.org/3/library/multiprocessing.html) used. We recommand to use the same number as you're odoo workers minus 1, in our case it's 8 so I'll use `7` process.
* Limit: This arguments is the number of cities PER process, if you set 7 process and 5 cities limit you'll export 7*5=35 different cities. In our example we don't use this option so it will be automaticaly set according to the departement sizes.
* Nd: Alias No-Delete, if you provide this argument the database won't be deleted at the end of the export, so you'll get the oportunity to go through the Odoo database.

```bash
mycityco2 run <importer> --departement=<departement> --process=<process> --limit=<limit> -nd
```

### Merging CSV
Command: csv

Description: This command merge the output csv in order to have only 1 final CSV and not the number of database.

Argument:

* Merge: Alias m. This argument is used to merge the csv together. You need to add this argument to really merge the CSV to 1 final.
* Delete: Alias d. If you want to delete the old csv after merging than provide this argument
* Name: Alias n. You need to provide this argument in order tho customize the merged csv.
* Move: If you provide this argument than the older CSV to an 'archive' folder. Do not use with delete.

```bash
mycityco2 csv --merge --delete --name=<name> --move
```