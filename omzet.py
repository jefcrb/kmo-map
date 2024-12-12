# dit script kijkt naar alle bedrijven in je postcode en voegt hun omzet van vorig jaar toe

# bijna klaar, zie lijk 80 ongv. omzet is de omzet van entiteitnummer. moet dat nu nog in een csv file krijgen.


import pandas as pd
import requests
from io import BytesIO

def fetch_company_data(enterpriseNumber):

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        # Make the GET request
        response = requests.get(f"https://consult.cbso.nbb.be/api/rs-consult/published-deposits?page=0&size=10&enterpriseNumber={enterpriseNumber}&sort=periodEndDate,desc&sort=depositDate,desc", headers=headers)

        
        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            # print("Data fetched successfully:")
            # print(data)
            return data
        else:
            # print(f"Failed to fetch data. Status code: {response.status_code}")
            # print(response.text)
            pass
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


def fetch_omzet_data(id):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://consult.cbso.nbb.be/api/external/broker/public/deposits/consult/csv/{id}"
        
    try:
        # Make the GET request to the API
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Print the content of the response
            # print(response.text)
            data = pd.read_csv(BytesIO(response.content),names=["Key", "Value"])
            return data
        # else:
            # print(f"Failed to fetch data. Status code: {response.status_code}")

    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    input_file = "./data_2060/address.csv"
    output_file = "./data_2060/idkWhereThisComesFrom.csv"

    # Read address data
    address_data = pd.read_csv(input_file)

    i = 0
    for entitynumber in address_data['EntityNumber']:
        data = fetch_company_data(entitynumber.replace(".","")) # krijg de data over het bedrijf

        if data is not None:        # soms krijg je een none
            if "content" in data:   # effe checken dat er wel content is
                if len(data["content"])>0:      # soms is er geen data over het bedrijf. daar moeten we ook niets van opzoeken
                    # print(data["content"][0]["id"])         # dan hebben we index 0 nodig omdat dat altijd de recentste is en we zoeken de id voor de latere request.
                    id = data["content"][0]["id"]
                    omzet_csv = fetch_omzet_data(id)
                    if omzet_csv is not None:
                        if not omzet_csv[omzet_csv['Key'].str.startswith('20/58', na=False)].empty:
                            omzet = omzet_csv[omzet_csv['Key'].str.startswith('20/58', na=False)].iloc[0]["Value"]
                            print(entitynumber)
                            print(omzet)
                            with open("./data_2060/EntityNumber_with_omzet.csv","a") as file:
                                file.write(f"{entitynumber},{omzet}\n")
                            
    
    address_data.to_csv(output_file, index=False)


