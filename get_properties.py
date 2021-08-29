import json
import pandas as pd
import csv
import os

P_DIR = 'properties/'
BYTE_L = 5000 # used to label if document is available

if not os.path.exists(P_DIR):
    os.mkdir(P_DIR)

with open('file2txtlog.json', encoding='utf-8') as f:
    file = json.load(f)
docx = []
pdf = []
for x in file['handled']:
    if x['Content-Type'].split('/')[-1]=='docx':
        docx.append(x)
    elif x['Content-Type'].split('/')[-1]=='pdf':
        pdf.append(x)
    else:
        print('Unhandled content type.')

keys = set().union(*(d.keys() for d in docx))
with open(P_DIR+'docx.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(docx)
keys = set().union(*(d.keys() for d in pdf))
with open(P_DIR+'pdf.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(pdf)

docxdf = pd.read_csv(P_DIR+'docx.csv', encoding='utf-8')
pdfdf = pd.read_csv(P_DIR+'pdf.csv', encoding='utf-8')

bigdfcols = ['pagec', 'content_type', 'type', 'agency', 'dest', 'byte_len']
docscols = ['Pages','Content-Type', 'type', 'path', 'dest', 'byteLen']
pdfcols = ['NPages','Content-Type', 'type', 'path', 'dest', 'byteLen']

bigdf = pd.DataFrame(columns=bigdfcols)

docxdf = docxdf.rename({x:y for x, y in zip(docscols, bigdfcols)}, axis=1)
pdfdf = pdfdf.rename({x:y for x, y in zip(pdfcols, bigdfcols)}, axis=1)

bigdf = bigdf.append(docxdf[bigdfcols], ignore_index=True)
bigdf = bigdf.append(pdfdf[bigdfcols], ignore_index=True)

bigdf['is_avail'] = bigdf['byte_len']>=BYTE_L
bigdf['content_type'] = bigdf['content_type'].str.split(pat='/', expand=True)[1]
bigdf['dest'] = bigdf['dest'].str.split(pat='/', expand=True, n=1)[1]
bigdf[['agency', 'fn']] = bigdf['agency'].str.split(pat='/', expand=True)[[1,2]]

typecor = {i-1:x for i, x in enumerate(['N/A', 'Executive Summary', 'Audit Report', 'ML', 'Management Letter', 'Observations'])}

bigdf['type_text'] = bigdf['type'].apply(lambda x: typecor[x])

bdt = pd.DataFrame() # breakdown by type
bdt['pagec'] = bigdf.groupby('type')['pagec'].sum()
bdt[['docx_count','pdf_count']] = bigdf.groupby('type')['content_type'].value_counts().unstack(level=1).fillna(0)[['docx', 'pdf']]
bdt['total_docs'] = bdt['docx_count']+bdt['pdf_count']

bigdf.to_csv(P_DIR+'bigdf.csv', encoding='utf-8', index=False)
bdt.to_csv(P_DIR+'bdt.csv', encoding='utf-8', index=True)
