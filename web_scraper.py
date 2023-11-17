import json

# A function to execute script (JS)
def execute_script(browser, js_file):
    f = open(js_file, 'r')
    json_string = browser.execute_script(f.read())
    f.close()

    return json.loads(json_string)
    

# A function to sleep (scraping ethics)

# Pass in the URL

# Start here