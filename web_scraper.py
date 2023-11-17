import json
import time
import random

from selenium import webdriver
from pprint import pprint

def execute_script(browser, js_file):
    f = open(js_file, 'r')
    json_string = browser.execute_script(f.read())
    f.close()

    return json.loads(json_string)
    
def polite_delay():
    delay_time = random.uniform(1,5)
    time.sleep(delay_time)
    return None

# Pass in the URL
def perform_scraping(url_list):

    # We don't want to open the browser
    browser = webdriver.Chrome()
    product_list = []

    for url in url_list:
        browser.get(url)
        time.sleep(10)

        nutrition_info = execute_script(browser, 'scrapers/woolworth_scraper.js')
        product_list.append(nutrition_info)
        
        polite_delay()

    return None

# Start here
url_list = [
    "https://www.woolworths.com.au/shop/productdetails/84628/arnott-s-tim-tam-original-family-pack-chocolate-biscuits",
    "https://www.woolworths.com.au/shop/productdetails/172660/woolworths-cashews-roasted-salted"
]

perform_scraping(url_list)