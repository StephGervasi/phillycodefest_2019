__author__ = 'Victor Ruiz, ruizv1@email.chop.edu'
import pandas as pd
import json
#pd.set_option("display.max_columns", None)
pd.set_option("mode.chained_assignment", 'raise')


def main():
    ### load food demand geolocation data
    data_path = "/Users/ruizv1/GitRepos/phillycodefest_2019/LNA_HP_Food_Access.geojson"
    with open(data_path, 'r') as f:
        data = json.load(f)

    for feature in data['features']:
        print(5)
    print(5)


if __name__ == '__main__':
    main() 