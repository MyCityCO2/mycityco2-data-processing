i=1;
j=$#;
while [ $i -le $j ]
do
    echo "Instance n*$i - Running departement $1";
    poetry run mycityco2 run fr --departement=$1 -f;
    poetry run mycityco2 csv -m -n Departement-$1 --move;
    i=$((i + 1));
    shift 1;
done
