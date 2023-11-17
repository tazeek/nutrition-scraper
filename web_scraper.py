from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import json
import time
import random
import pandas as pd

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

        # Selenium only waits for the HTML DOM to load.
        # We are scraping dynamically loaded content so we have to 
        # explicitly make Selenium wait until this is loaded
        # Wait until the presence of a HTML element with the class 'paging-next' is detected
        try:
            timeout = 10
            WebDriverWait(browser, timeout).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'ar-product-details-nutrition-table')
            ))
        except TimeoutException:
             pass

        nutrition_info = execute_script(browser, 'scrapers/woolworth_scraper.js')
        product_list.append(nutrition_info)

        polite_delay()

    #pprint(product_list)

    return product_list

# Start here
url_list = [
    "https://www.woolworths.com.au/shop/productdetails/84628/arnott-s-tim-tam-original-family-pack-chocolate-biscuits",
    "https://www.woolworths.com.au/shop/productdetails/172660/woolworths-cashews-roasted-salted"
]

product_list = perform_scraping(url_list)

column_names = list(product_list[0].keys())
print(column_names)