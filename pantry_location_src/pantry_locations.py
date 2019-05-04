__author__ = 'Victor Ruiz, ruizv1@email.chop.edu'
import pandas as pd
from geopy.geocoders import Nominatim
#pd.set_option("display.max_columns", None)
pd.set_option("mode.chained_assignment", 'raise')
import numpy as np
import re
from tqdm import tqdm

def address2coordinates(geolocator, address, city, state, zip, country_code="us", silent_fail=False):
    query = {
        'street': address, 'city': city, 'state': state, 'postalcode': zip, 'country_code': country_code
    }
    location = geolocator.geocode(query)
    try:
        lat, long = location.latitude, location.longitude
        return lat, long
    except:
        if silent_fail:
            return np.nan, np.nan
        else:
            raise ValueError("Address could not be converted to lat/long")

def main():
    #### read text file with pantry locations
    with open('pantry_locations_coalition_against_hunger.txt') as f:
        locations_txt = f.read()
    locations_list = re.split(r'Read More', locations_txt)

    ### create a df with locations
    df = pd.DataFrame(columns=['name', 'address', 'city', 'state', 'zip', 'days_open'])
    geolocator = Nominatim(user_agent="food_safety_locator")
    for location in locations_list:
        #make sure location has proper format
        location_lines = [var for var in re.split(r'\n', location) if var != '']
        if len(location_lines) != 5:
            continue # poorly-formatted location address

        #get location details
        name = location_lines[0].strip()
        address = location_lines[2].strip()
        city, state_zip = re.split(',', location_lines[3].strip())
        state, zip = re.split(r'\s+', state_zip.strip())
        days_open = re.split(r',\s+', location_lines[4].replace('Open: ', ''))

        df = df.append(pd.Series({
            'name': name, 'address': address, 'city': city, 'state': state, 'zip': zip, 'days_open': days_open
        }), ignore_index=True, sort=True)

    ### get coordinates of each location
    tqdm.pandas()
    df[['latitude', 'longitude']] = df.progress_apply(
        lambda x: pd.Series(address2coordinates(
            geolocator=geolocator, address=x['address'], city=x['city'], state=x['state'], zip=x['zip'],
            country_code="us", silent_fail=True
        )), axis=1
    )

    df = df[df.latitude.notnull()][['name', 'address', 'city', 'state', 'zip', 'days_open', 'latitude', 'longitude']]
    ### save output
    df.to_pkl("pantry_location_dataset.pkl")
    df.to_csv("pantry_location_dataset.csv", index=False)

if __name__ == '__main__':
    main() 