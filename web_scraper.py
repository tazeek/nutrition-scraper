from bs4 import BeautifulSoup as soup

import requests
import time
import re
import json
import pandas as pd

class NutriScraper:

    def __init__(self):

        self._header = {
            'User-Agent': 'Mozilla/5.0'
        }

    @classmethod
    def get_value_html(cls, serve_str):
        return serve_str.split(':')[1].strip()

    @classmethod
    def get_text(cls, nutri_val):
        return re.sub('[^a-zA-Z ]', '', nutri_val).strip()
    
    @classmethod
    def clean_prefix_values(cls, nutri_val):
        return re.sub(r'^\D*', '', nutri_val)  

    @classmethod
    def get_number(cls, nutri_val):
        return re.search(r'\d+(\.\d+)?', nutri_val).group() \
            if nutri_val else 0
    
    @classmethod
    def _polite_delay(cls, amount):
        time.sleep(amount)
        return None

    # Pass in the URL
    def perform_scraping(self, url):

        nutrition_dict = {}

        # Extract the html first
        response = requests.get(url, headers=self._header)
        page_soup = soup(response.text, 'html.parser')

        # Get the product name
        product_name = page_soup.find_all("h1", {"class": "shelfProductTile-title heading4"})
        nutrition_dict['Product Name'] = product_name[0].get_text()

        # Get the serving pack
        # NOTE: Some products leave it out. So, give it a value of 1
        servings_pack = page_soup.find("div", {"*ngif": 'productServingsPerPack'})
        servings_pack_value = self.get_value_html(servings_pack.get_text()) if servings_pack else 1
        nutrition_dict['Servings per pack'] = servings_pack_value

        # Get the money
        dollar_amount = page_soup.find("span", {"class": "price-dollars"})
        cents_amount = page_soup.find("span", {"class": "price-cents"})
        nutrition_dict['Price'] = f"{dollar_amount.get_text()}.{cents_amount.get_text()}"

        # Get the serving size, followed by the metrics
        serving_size = page_soup.find("div", {"*ngif": 'productServingSize'})
        serving_size = self.get_value_html(serving_size.get_text())

        serving_size_metric = self.get_text(serving_size) 
        serving_size_value = self.get_number(serving_size)
        nutrition_dict[f'Serving size {serving_size_metric}'] = serving_size_value

        nutrition_dict['Pack Size'] = float(serving_size_value) * float(servings_pack_value)

        nutrition_row = page_soup.find_all("ul", {"class": 'wow-row nutrition-row'})

        for row in nutrition_row:

            nutrition_vals = row.find_all("li", {"class": 'wow-col-4 nutrition-column'})
            nutrition_vals = [val.get_text().strip() for val in nutrition_vals]

            # Get the nutrition label
            nutrition_label = self.get_text(nutrition_vals[0].strip())

            # Get the metric and the respective numbers
            serving_quantity = self.clean_prefix_values(nutrition_vals[1])
            serving_per_100 = self.clean_prefix_values(nutrition_vals[2])

            metric = self.get_text(serving_quantity)

            serving_quantity = self.get_number(serving_quantity)
            serving_per_100 = self.get_number(serving_per_100)

            nutrition_dict[f'{nutrition_label} per serving ({metric})'] = serving_quantity
            nutrition_dict[f'{nutrition_label} per 100g/100mL ({metric})'] = serving_per_100

        self._polite_delay(20)

        # Call the API too
        # The ID is the second-last before the product name
        product_id = url.split("/")[-2]
        new_url = f'https://www.woolworths.com.au/api/v3/ui/schemaorg/product/{product_id}'
        response = requests.get(new_url, headers=self._header)
        product_info_dict = json.loads(response.content)

        # Get the price
        nutrition_dict['Price'] = product_info_dict["offers"]["price"]

        # Respect the scraping etiquettes :)
        self._polite_delay(20)

        return nutrition_dict
