# pd-subcategory
# pd-filebox

from bs4 import BeautifulSoup
import requests
import json

ROOT = 'https://coa.gov.ph'
MAIN_PAGE = r'https://coa.gov.ph/index.php/national-government-agencies/2020'

maindir = BeautifulSoup(requests.get(MAIN_PAGE).text, 'html.parser')
ga2link = [(x.text, x['href']) for x in maindir.select('.pd-subcategory > a')]

filetree = {}
FILE2LINK = {}

def getFiles(bs4obj):
    li = []
    fs = [(x.text, x['href']) for x in bs4obj.select('.pd-float > a')]
    if len(fs)==0:
        raise Exception("Error, no files found!")
    for fname, flink in fs:
        li.append(fname)
        FILE2LINK[fname] = flink
        print(f'-->Found {fname} at {flink}')
    return li

for aname, alink in ga2link:
    alink +='?limit=all'
    print(f'Ripping {aname} at {alink}')
    cat = BeautifulSoup(requests.get(ROOT+alink).text, 'html.parser')
    subcat = [(x.text, x['href']) for x in cat.select('.pd-subcategory > a')]
    if len(subcat) > 0:
        filetree[aname] = {}
        for sname, slink in subcat:
            slink +='?limit=all'
            print(f'-> Subcat: {sname} at {slink}')
            files = BeautifulSoup(requests.get(ROOT+slink).text, 'html.parser')
            filetree[aname][sname] = getFiles(files)

    else:
        filetree[aname] = getFiles(cat)

with open('fstruct.json', 'w', encoding='utf-8') as f:
    json.dump(filetree, f)
with open('links.json', 'w', encoding='utf-8') as f:
    json.dump(FILE2LINK, f)
