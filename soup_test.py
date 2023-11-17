import requests
from bs4 import BeautifulSoup as soup
import time
import re

def get_value_html(serve_str):
    return serve_str.split(':')[1].strip()

def get_metric(nutri_val):
    return re.sub('[^a-zA-Z]', '', nutri_val)

def get_number(nutri_val):
    return re.findall("\d+\.\d+", nutri_val)[0]

url = 'https://www.woolworths.com.au/shop/productdetails/84628/arnott-s-tim-tam-original-family-pack-chocolate-biscuits'

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

page_soup = soup(response.text, 'html.parser')

# Get the product name
product_name = page_soup.find_all("h1", {"class": "shelfProductTile-title heading4"})
product_name = product_name[0].get_text()

# Get the serving pack
servings_pack = page_soup.find("div", {"*ngif": 'productServingsPerPack'})
servings_pack = get_value_html(servings_pack.get_text())
print(f'Serving pack : {servings_pack}')

# Get the serving size
serving_size = page_soup.find("div", {"*ngif": 'productServingSize'})
serving_size = get_value_html(serving_size.get_text())

metric = get_metric(serving_size) 
value = get_number(serving_size)
print(f'Serving size {metric}: {value}')

#nutrition_row = page_soup.find_all("ul", {"class": 'wow-row nutrition-row'})

#for row in nutrition_row:

#    granular_vals = row.find_all("li", {"class": 'wow-col-4 nutrition-column'})
#    granular_vals = [val.get_text().strip() for val in granular_vals]
#    print(granular_vals)
#    print("\n\n")

time.sleep(10)

