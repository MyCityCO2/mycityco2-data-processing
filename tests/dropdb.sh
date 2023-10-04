i=1;
j=$#;
while [ $i -le $j ]
do
    n=1;
    while [ $n -le 7 ]
    do
        echo "Dropping gca_co2_$1-$n-test";
        dropdb "gca_co2_$1-$n-test";
        n=$((n + 1));
    done
    i=$((i + 1));
    shift 1;
done
