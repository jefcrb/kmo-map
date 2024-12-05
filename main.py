import csv
from geopy.geocoders import Nominatim

def geocode_addresses(input_csv, output_csv):
    # Initialize the geocoder
    geolocator = Nominatim(user_agent="geoapp")

    # Open the input CSV file
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        # Get fieldnames from the input CSV and add new ones for output
        fieldnames = reader.fieldnames + ['Latitude', 'Longitude']
        
        # Open the output CSV file
        with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            # Process each row
            for row in reader:
                address = row.get('Address')  # Adjust 'Address' to match the actual column name
                try:
                    # Geocode the address
                    location = geolocator.geocode(address)
                    if location:
                        row['Latitude'] = location.latitude
                        row['Longitude'] = location.longitude
                    else:
                        row['Latitude'] = None
                        row['Longitude'] = None
                except Exception as e:
                    print(f"Error geocoding address {address}: {e}")
                    row['Latitude'] = None
                    row['Longitude'] = None

                # Write the row to the output CSV
                writer.writerow(row)

# Specify the input and output CSV files
input_csv = 'address.csv'
output_csv = 'geocoded_addresses.csv'

# Call the function
geocode_addresses(input_csv, output_csv)
