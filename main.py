import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from geocode import geocode
import os

real_estate_properties = None

for i in range(55, 60):
    # URL of the page you want to scrape
    url = f'https://www.immobiliare.it/vendita-case/milano/?criterio=rilevanza&pag={i}'

    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the elements containing the properties' information
    # This is a generic example; you'll need to adjust selectors based on your target website
    if real_estate_properties is not None:
        real_estate_properties += soup.find_all('li', class_='nd-list__item in-reListItem')
    else:
        real_estate_properties = soup.find_all('li', class_='nd-list__item in-reListItem')

    time.sleep(5)

print(f"Number of properties: {len(real_estate_properties)}")
data = []
filename = 'milan_properties.csv'

# Check if the CSV file exists
if os.path.exists(filename):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filename)
    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
else:
    print("The file does not exist.")

count = 0
for real_estate_property in real_estate_properties:
    try:
        count += 1
        print(f"=================== {count}")
        # print(real_estate_property.prettify())

        # Price
        price = real_estate_property.find('div', class_="in-reListCardPrice").text
        print(f"price = {price}")

        # Size
        size = None
        card_feature_list = real_estate_property.find_all('div', class_='in-reListCardFeatureList__item')
        for item in card_feature_list:
            use = item.find('use')
            xlink_href = use.get('xlink:href')
            if xlink_href == '#size':
                size = item.text
                break
        print(f"size = {size}")

        # Address
        address = real_estate_property.find('a', class_="in-reListCard__title is-spaced").get('title')
        print(f"address = {address}")

        # Price per square meter
        price_float = float(re.search(r'(\d+(?:\.\d+)*)', price).group().replace('.', ""))
        # print(f"price_float = {price_float}")
        size_float = float(re.search(r'\d+(\.\d+)?', size).group())
        # print(f"size_float = {size_float}")
        price_per_square_meter_int = int(round(price_float / size_float))
        # print(f"price_per_square_meter_float = {price_per_square_meter_float}")
        price_per_square_meter = f"€{round(price_per_square_meter_int, 2)} / m^2"
        print(f"price_per_square_meter = {price_per_square_meter}")

        # Coordinates
        coordinates = geocode(address).split(':')
        latitude = coordinates[0]
        longitude = coordinates[1]
        print(f"latitude = {latitude}")
        print(f"longitude = {longitude}")

        # Calculate price per square meter if possible
        # You might need to clean and convert the data to perform calculations

        data.append({
            'Price': price,
            'Size': size,
            'Address': address,
            'Price Per Square Meter': price_per_square_meter,
            'Price Per Square Meter Integer': price_per_square_meter_int,
            'Latitude': latitude,
            'Longitude': longitude
        })
    except Exception as e:
        print(f"An error occurred: {e}")

# Convert the list of dictionaries into a DataFrame
df = pd.DataFrame(data)

# Export to CSV
df.to_csv('milan_properties.csv', index=False)
