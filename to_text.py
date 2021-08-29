import multiprocessing as mp
import os
import json
from docx2python import docx2python # https://github.com/ShayHill/docx2python
from tika import parser
from win32com import client as wc
import re


DEST = 'pdfs/'
TXT_PATH = 'txt/'
AUD_DOC = re.compile('(Executive[ _]*Summary)|(Audit[ _]*Report)|(ML)|(Management[ _]*Letter)|(Observations)')
ABS_PATH = os.getcwd()

def docxparser(docx, dest, ftype, doc=False):
    try:
        with open(dest, 'w', encoding='utf-8') as f:
            docu = docx2python(docx)
            pagec = docu.properties.get('Pages', -1)
            f.write(docu.text)
            docu.properties['Content-Type'] = "application/" + docx.rsplit('.', maxsplit=1)[-1]
            docu.properties['fromDoc'] = doc
            docu.properties['type'] = ftype
            docu.properties['path'] = docx
            docu.properties['dest'] = dest
            docu.properties['byteLen'] = utf8len(docu.text)
            return docu.properties
    except Exception as e:
        return 'Error:' + str(e) + ' ' + docx
    
def utf8len(s):
    return len(s.encode('utf-8'))

def pdfparser(pdf, dest, ftype):
    with open(pdf, 'rb') as f:
        with open(dest, 'w', encoding='utf-8') as g:
            par = parser.from_file(pdf)
            cont = par['content']
            g.write(cont)
            par['metadata']['type'] = ftype
            par['metadata']['path'] = pdf
            par['metadata']['dest'] = dest
            par['metadata']['byteLen'] = utf8len(par['content'])
            return {key.split(':')[-1]:val for key, val in par['metadata'].items()}

def docparser(doc, dest, ftype):
    # not optimal but working :P
    try:
        f = open(doc+'x', 'r')
        f.close()
    except:
        d = doc.split('/')
        pathh = [ABS_PATH]+d
        finald = d[-1]+'x'
        w = wc.Dispatch('Word.Application')
        wb = w.Documents.Open(os.path.join(*pathh))
        try:
            wb.SaveAs(os.path.join(*pathh[:-1],finald),16)
            w.close()
        except Exception as e:
            return 'Error:' + str(e) + ' ' + os.path.join(*pathh[:-1],finald)
    else:
        return docxparser(doc+'x', dest, ftype, doc=True)

def cant(a,b):
    return 'Can\'t handle this yet. ' + a.split('.')[-1]

def get_type(matchobj):
    if matchobj is None:
        return None
    for index, matchstr in enumerate(matchobj.groups()):
        if matchstr is not None:
            return index
    return None

HANDLERS = {'doc':docparser, 'docx':docxparser, 'pdf':pdfparser}

def parse2txt_worker(comnfile):
    com, file = comnfile
    com = com.strip().replace('"', '')
    src = DEST+com+'/'
    dest = TXT_PATH+com+'/'
    if not os.path.exists(dest):
        os.mkdir(dest.encode('utf-8'))
    filentypes = sorted(filter(lambda x: x[1] is not None, [(x,get_type(AUD_DOC.search(x))) for x in os.listdir(src)]), key=lambda x: x[1])
    for file, ftype in filentypes:
        try:
            file_ext = file.rsplit('.', maxsplit=1)[-1]
            return HANDLERS.get(file_ext)(src+file, dest+'summary.txt', ftype=ftype)
        except Exception as e:
            return 'Error 1:' + str(e)
    
    if len(os.listdir(src))==1:
        file = os.listdir(src)[0]
        file_ext = file.rsplit('.', maxsplit=1)[-1]
        return HANDLERS.get(file_ext)(src+file, dest+'summary.txt', ftype=-1)
    return str({com:os.listdir(src)})

def poolman(dest):
    comnfile = {}
    with open('com2zip.json', 'r', encoding='utf-8') as f:
        comnfile = json.load(f)
    procnum = min(mp.cpu_count(), len(comnfile))
    pool = mp.Pool(procnum)
    res = pool.map(parse2txt_worker, list(comnfile.items()), chunksize=round(len(comnfile)/procnum))
    pool.close()
    return res

if __name__=="__main__":
    if not os.path.exists(TXT_PATH):
        os.mkdir(TXT_PATH.encode('utf-8'))
    unhandled = poolman(TXT_PATH)
    outjson = {'handled':[], 'unhandled':[]}
    for x in unhandled:
        if x is None:
            pass
        if type(x) is str:
            outjson['unhandled'].append(x)
        else:
            outjson['handled'].append(x)
    with open('file2txtlog.json', 'w', encoding='utf-8') as f:
        json.dump(outjson, f)
