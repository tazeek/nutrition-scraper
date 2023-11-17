import json
import time
import random

from selenium import webdriver

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

# Start here