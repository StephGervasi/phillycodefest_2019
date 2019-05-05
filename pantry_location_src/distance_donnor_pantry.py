__author__ = 'Victor Ruiz, ruizv1@email.chop.edu'
import pandas as pd
import json
#pd.set_option("display.max_columns", None)
pd.set_option("mode.chained_assignment", 'raise')
from geopy.distance import geodesic
from geojson import Feature, FeatureCollection, Point
from pyzipcode import ZipCodeDatabase

def coordinates_from_zip(zip_code):
    zcdb = ZipCodeDatabase()
    zipcode = zcdb[zip_code]
    return zipcode.latitude, zipcode.longitude

def compute_distance(from_lat, from_long, to_lat, to_long, verbose=False):
    '''
    computes the distance between two sets of coordinates
    :param from_lat:
    :param from_long:
    :param to_lat:
    :param to_long:
    :param verbose:
    :return:
    '''
    from_xy = (from_lat, from_long)
    to_xy = (to_lat, to_long)
    distance = geodesic(from_xy, to_xy).miles
    if verbose:
        print("Distance from: {},{} to: {},{} is {} miles".format(from_lat, from_long, to_lat, to_long, distance))
    return distance

def distance_to_pantries(from_lat, from_long, pantries):
    '''
    computes the distance from a location coordinates to all available food pantries
    :param from_lat:
    :param from_long:
    :param pantries:
    :return:
    '''
    distances = pantries[['name', 'address', 'latitude', 'longitude']].copy()
    distances.loc[:, 'distance'] = distances.apply(lambda x: compute_distance(
        from_lat, from_long, x['latitude'], x['longitude']
    ), axis=1)
    return distances

def pantry_distances_to_geojson(distances):
    features = distances.apply(
        lambda row: Feature(geometry=Point((float(row['longitude']), float(row['latitude'])))),
    axis=1).tolist()
    properties = distances.drop(['latitude', 'longitude'], axis=1).to_dict('records')
    feature_collection = FeatureCollection(features=features, properties=properties)
    return feature_collection


def main():
    ### read dataset with locations
    df = pd.read_csv("pantry_location_dataset.csv")
    from_location = df.iloc[0]
    to_location = df.iloc[1]

    user_distances = distance_to_pantries(from_location.latitude, from_location.longitude, df)
    geojson_obj = pantry_distances_to_geojson(user_distances)
    with open("distances_gojson.geojson" ,'w') as out_f:
        json.dump(geojson_obj, out_f)


if __name__ == '__main__':
    main() 