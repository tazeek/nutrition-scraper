import requests
from bs4 import BeautifulSoup as soup
import time

def get_number(serve_str):
    return serve_str.split(':')[1].strip()

def get_metric():
    ...

url = 'https://www.woolworths.com.au/shop/productdetails/84628/arnott-s-tim-tam-original-family-pack-chocolate-biscuits'

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

page_soup = soup(response.text, 'html.parser')

# Get the product name
product_name = page_soup.find_all("h1", {"class": "shelfProductTile-title heading4"})
product_name = product_name[0].get_text()

# Get the serving pack
servings_pack = page_soup.find("div", {"*ngif": 'productServingsPerPack'})
servings_pack = get_number(servings_pack.get_text())
print(f'Serving pack: {servings_pack}')
#print(servings_pack.get_text().strip())

# Get the serving size
#serving_size = page_soup.find("div", {"*ngif": 'productServingSize'})
#print(serving_size.get_text())

#nutrition_row = page_soup.find_all("ul", {"class": 'wow-row nutrition-row'})

#for row in nutrition_row:

#    granular_vals = row.find_all("li", {"class": 'wow-col-4 nutrition-column'})
#    granular_vals = [val.get_text().strip() for val in granular_vals]
#    print(granular_vals)
#    print("\n\n")

time.sleep(10)

