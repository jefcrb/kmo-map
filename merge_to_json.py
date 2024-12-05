# deze file merged alle data van de bedrijven in 1 json file

import pandas as pd
import json

# File paths
address_file = "./data_2060/address_with_latlon.csv"
contact_file = "./data_2060/contact.csv"
denomination_file = "./data_2060/denomination.csv"
output_file = "./data_2060/data.json"

# Read CSV files
address_data = pd.read_csv(address_file)
contact_data = pd.read_csv(contact_file)
denomination_data = pd.read_csv(denomination_file)

# Group contact data by EntityNumber and merge ContactType and Value
def merge_contacts(df):
    grouped = df.groupby("EntityNumber").apply(lambda x: x.to_dict(orient="records"))
    return grouped.apply(lambda x: {row["ContactType"]: row["Value"] for row in x}).to_dict()

merged_contacts = merge_contacts(contact_data)

# Merge data on 'EntityNumber'
address_data = address_data.set_index("EntityNumber")
denomination_data = denomination_data.set_index("EntityNumber")

# Combine address and denomination data
merged_data = address_data.join(denomination_data, how="left").reset_index()

# Add contact information to merged data
merged_data["Contacts"] = merged_data["EntityNumber"].apply(lambda x: merged_contacts.get(x, {}))

# Replace NaN with empty string for JSON serialization
merged_data = merged_data.fillna("")

# Convert merged data to JSON
data_json = merged_data.to_dict(orient="records")

# Save JSON data to file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)

print(f"Data merged and saved to {output_file}")
