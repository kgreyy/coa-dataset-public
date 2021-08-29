import json
import requests as r
import os
import random

ROOT_URL = 'https://coa.gov.ph'
# ZIP_PATH = 'zips/'
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


if not os.path.exists(ZIP_PATH):
    os.mkdir(ZIP_PATH.encode('utf-8'))
    
with open('links.json', 'r') as f:
    dep2link = json.load(f)

com2zip = {}
i = 0
# one process download to not overload COA :)
for com, link in dep2link.items():
    h = r.head(ROOT_URL + link)
    fn = h.headers.get('content-disposition').split("=")[-1].strip('"')
    com2zip[com] = fn.strip('"')
    
    if os.path.isfile(ZIP_PATH+fn):
        print(f"Skipping {fn}...")
        continue
    
    user_agent = random.choice(user_agent_list)
    obj = r.get(ROOT_URL + link, headers={'User-Agent': user_agent})
    print(f"Downloading {fn}...")

    with open(ZIP_PATH+fn, 'wb') as f:
        f.write(obj.content)

with open('com2zip.json', 'w', encoding='utf-8') as f:
    json.dump(com2zip, f)
