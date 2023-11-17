from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import json
import time
import random
import pandas as pd

class NutriScraper:

    def __init__(self):

        self._browser = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            )
        )

    def _execute_script(self, js_file):

        json_string = ''

        with open(js_file, 'r') as f:
            json_string = self._browser.execute_script(f.read())

        return json.loads(json_string)
    
    @classmethod
    def _polite_delay(cls):
        delay_time = random.uniform(1,5)
        time.sleep(delay_time)
        return None

    # Pass in the URL
    def perform_scraping(self, url):

        self._browser.get(url)

        # Selenium only waits for the HTML DOM to load.
        # We are scraping dynamically loaded content so we have to 
        # explicitly make Selenium wait until this is loaded
        # Wait until the presence of a HTML element with the class 
        # 'ar-product-details-nutrition-table' is detected (Nutrition Table)
        try:
            timeout = 20
            WebDriverWait(self._browser, timeout).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'ar-product-details-nutrition-table')
            ))
        except TimeoutException:
            pass

        nutrition_info = self._execute_script('scrapers/woolworth_scraper.js')

        # Respect the scraping etiquettes :)
        self._polite_delay()

        return nutrition_info
