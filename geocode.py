# dit script maakt een nieuwe csv "adress_with_latlon.csv" naast al je postcode data.
# deze csv bevat de latitude & longtitude van elk bedrijf.

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# Function to fetch latitude and longitude
def get_lat_lon(geolocator, address):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        time.sleep(1)
        return get_lat_lon(geolocator, address)  # Retry on timeout
    return None, None

# File paths
input_file = "./data_2060/address.csv"
output_file = "./data_2060/address_with_latlon.csv"

# Read address data
address_data = pd.read_csv(input_file)

# Initialize geolocator
geolocator = Nominatim(user_agent="address-geocoder")

# Prepare address strings
address_data["FullAddress"] = (
    address_data["StreetNL"].fillna("") + " " +
    address_data["HouseNumber"].fillna("").astype(str) + ", " +
    address_data["Zipcode"].fillna("").astype(str) + " " +
    address_data["MunicipalityNL"].fillna("") + ", Belgium"
)

# Fetch latitude and longitude
latitudes = []
longitudes = []

print("Fetching latitude and longitude for each address...")
for index, row in address_data.iterrows():
    address = row["FullAddress"]
    lat, lon = get_lat_lon(geolocator, address)
    latitudes.append(lat)
    longitudes.append(lon)
    print(f"Processed {index + 1}/{len(address_data)}: {address} -> {lat}, {lon}")

# Add latitude and longitude to the dataframe
address_data["Latitude"] = latitudes
address_data["Longitude"] = longitudes

# Save the updated dataframe to a new file, including 'EntityNumber'
address_data.to_csv(output_file, index=False)

print(f"File with latitude and longitude saved to {output_file}")
