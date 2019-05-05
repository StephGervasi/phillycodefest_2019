__author__ = 'Victor Ruiz, ruizv1@email.chop.edu'
import pandas as pd

#pd.set_option("display.max_columns", None)
pd.set_option("mode.chained_assignment", 'raise')
from pantry_location_src.distance_donnor_pantry import distance_to_pantries, coordinates_from_zip

def main():
    ### read zip_code
    zip_code = 19146
    lat, long = coordinates_from_zip(zip_code)

    ### load pantry location
    pantries = pd.read_csv("pantry_location_dataset.csv")

    ### compute distance from zip code to all pantries
    distances = distance_to_pantries(lat, long, pantries)

    ### sort and get closest 5 pantries
    distances = distances.sort_values('distance', ascending=True).iloc[0:5]

    print(distances)


if __name__ == '__main__':
    main() 