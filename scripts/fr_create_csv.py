# NOT FINISHED

import requests

url = "https://data.economie.gouv.fr/api/v2/catalog/datasets/balances-comptables-des-communes-en-{}/exports/csv?offset=0&timezone=UTC&limit=-1"

# YEAR = list(range(2010, 2022)) #2010 to 2021
YEAR = [2010]  # 2010 to 2021

DEPARTEMENT = ["01"]

for year in YEAR:

    refine_parameter = "&refine=budget:BP" if int(year) <= 2015 else "&refine=cbudg:1"
    refine_url = url.format(year) + refine_parameter

    for dep in DEPARTEMENT:
        dep_url = refine_url + f"&refine=ndept:{dep}"

        dept = requests.get(dep_url).content.decode("utf-8")

        with open(f"{year}-{dept}", "w") as f:
            f.write(dept)

        # print(dept)
    # print(refine_url)
