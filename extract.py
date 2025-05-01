import json
from bs4 import BeautifulSoup

with open('macrotrends_stock_screener.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

script_tags = soup.find_all('script')
print(len(script_tags))
for script_tag in script_tags:
    script_text = script_tag.string
    if script_text is None:
        continue
#   Locate the variable `originalData` in the script text
    variable_name = 'var originalData ='
    if variable_name in script_text:
        json_start = script_text.find(variable_name) + len(variable_name)
        json_end = script_text.find("}];", json_start) + 2
        json_data_str = script_text[json_start:json_end].strip()

        try :
            data = json.loads(json_data_str)
            print(json.dumps(data, indent = 4))
            print("total no. of objects = ", len(data))
            break
        except json.JSONDecodeError:
            print("Error: Invalid JSON format found. Skipping this script tag")
            continue

print("Finished processing script tags")