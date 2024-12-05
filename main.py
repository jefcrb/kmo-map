import os
import pandas as pd
import sys

input_dir = './data'

files = [
    "activity.csv",
    "address.csv",
    "contact.csv",
    "denomination.csv",
]

if len(sys.argv) < 2:
    print("Invalid input")
if len(sys.argv[1]) != 4:
    print("Invalid input")

output_dir = f'./data_{sys.argv[1]}'

os.makedirs(output_dir, exist_ok=True)

address_file = os.path.join(input_dir, "address.csv")
address_df = pd.read_csv(address_file)
filtered_entity_numbers = address_df[address_df["Zipcode"] == sys.argv[1]]["EntityNumber"].unique()

for file in files:
    input_file_path = os.path.join(input_dir, file)
    output_file_path = os.path.join(output_dir, file)
    
    df = pd.read_csv(input_file_path)
    
    filtered_df = df[df["EntityNumber"].isin(filtered_entity_numbers)]

    filtered_df.to_csv(output_file_path, index=False)

print(f"Filtered files have been written to {output_dir}")
