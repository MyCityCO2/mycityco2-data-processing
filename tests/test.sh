echo "Les departement choisi sont $1, $2, $3"

poetry run mycityco2 run --departement=$1
poetry run mycityco2 run --departement=$2
poetry run mycityco2 run --departement=$3

poetry run mycityco2 csv -m
