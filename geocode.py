# dit script maakt een nieuwe csv "adress_with_latlon.csv" naast al je postcode data.
# deze csv bevat de latitude & longtitude van elk bedrijf.

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

def get_lat_lon(geolocator, address):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        time.sleep(1)
        return get_lat_lon(geolocator, address)
    return None, None

input_file = "./data_2060/address.csv"
output_file = "./data_2060/address_with_latlon.csv"

address_data = pd.read_csv(input_file)

geolocator = Nominatim(user_agent="address-geocoder")

address_data["FullAddress"] = (
    address_data["StreetNL"].fillna("") + " " +
    address_data["HouseNumber"].fillna("").astype(str) + ", " +
    address_data["Zipcode"].fillna("").astype(str) + " " +
    address_data["MunicipalityNL"].fillna("") + ", Belgium"
)

latitudes = []
longitudes = []

print("Latitude en longitude voor alle adressen worden opgehaald...")
for index, row in address_data.iterrows():
    address = row["FullAddress"]
    lat, lon = get_lat_lon(geolocator, address)
    latitudes.append(lat)
    longitudes.append(lon)
    print(f"Processed {index + 1}/{len(address_data)}: {address} -> {lat}, {lon}")

address_data["Latitude"] = latitudes
address_data["Longitude"] = longitudes

address_data.to_csv(output_file, index=False)

print(f"Bestand met lat en lon opgeslagen in {output_file}")
