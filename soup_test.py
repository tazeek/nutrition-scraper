import requests
from bs4 import BeautifulSoup as soup
import time
import re

def get_value_html(serve_str):
    return serve_str.split(':')[1].strip()

def get_text(nutri_val):
    return re.sub('[^a-zA-Z ]', '', nutri_val).strip()

def get_number(nutri_val):
    return re.findall("\d+\.\d+", nutri_val)[0]

url = 'https://www.woolworths.com.au/shop/productdetails/84628/arnott-s-tim-tam-original-family-pack-chocolate-biscuits'

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

page_soup = soup(response.text, 'html.parser')

# Get the product name
product_dict = {}

product_name = page_soup.find_all("h1", {"class": "shelfProductTile-title heading4"})
product_dict['Product Name'] = product_name[0].get_text()

# Get the serving pack
servings_pack = page_soup.find("div", {"*ngif": 'productServingsPerPack'})
servings_pack_value = get_value_html(servings_pack.get_text())
product_dict['Servings per pack'] = servings_pack_value

# Get the serving size, followed by the metrics
serving_size = page_soup.find("div", {"*ngif": 'productServingSize'})
serving_size = get_value_html(serving_size.get_text())

serving_size_metric = get_text(serving_size) 
serving_size_value = get_number(serving_size)
product_dict[f'Serving size {serving_size_metric}'] = serving_size_value

product_dict['Pack Size'] = float(serving_size_value) * float(servings_pack_value)

nutrition_row = page_soup.find_all("ul", {"class": 'wow-row nutrition-row'})

for row in nutrition_row:

    granular_vals = row.find_all("li", {"class": 'wow-col-4 nutrition-column'})
    granular_vals = [val.get_text().strip() for val in granular_vals]

    nutrition = get_text(granular_vals[0].strip())
    print(nutrition)

    serving_per_pack = granular_vals[1]
    serving_per_100 = granular_vals[2]

    metric = get_text(serving_per_pack)
    print(metric)



    #print(granular_vals)
    print("\n\n")

time.sleep(10)

