# deze file merged alle data van de bedrijven in 1 json file

import pandas as pd
import json


address_file = "./data_2060/address_with_latlon.csv"
contact_file = "./data_2060/contact.csv"
denomination_file = "./data_2060/denomination.csv"
omzet_file = "./data_2060/EntityNumber_with_omzet.csv"
output_file = "./data_2060/data.json"

address_data = pd.read_csv(address_file)
contact_data = pd.read_csv(contact_file)
denomination_data = pd.read_csv(denomination_file)
omzet_data = pd.read_csv(omzet_file)

def merge_contacts(df):
    grouped = df.groupby("EntityNumber").apply(lambda x: x.to_dict(orient="records"))
    return grouped.apply(lambda x: {row["ContactType"]: row["Value"] for row in x}).to_dict()

merged_contacts = merge_contacts(contact_data)

address_data = address_data.set_index("EntityNumber")
denomination_data = denomination_data.set_index("EntityNumber")
omzet_data = omzet_data.set_index("EntityNumber")

merged_data = address_data.join([denomination_data, omzet_data], how="left").reset_index()

merged_data["Contacts"] = merged_data["EntityNumber"].apply(lambda x: merged_contacts.get(x, {}))

merged_data = merged_data.fillna("")

data_json = merged_data.to_dict(orient="records")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)

print(f"Gefilterde resultaten staan in {output_file}")
