import pandas as pd
import re
import os

P_DIR = 'properties/'
TXT_PATH = 'txt/'

# for EDA purposes
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv(P_DIR+'bigdf.csv')
cnt = []
mga = []

def get_text_op(x, **kwargs):
    with open(TXT_PATH+x, 'r', encoding='utf-8') as f:
        text = ' '.join(f.read().splitlines()) # small files anw
        words = exp.findall(text)
        return pd.Series([text, words, len(words)])

exp = re.compile('(\w+ )?opinion', re.IGNORECASE)
opinions = re.compile('\s?(unmodified)|(clean)|(unqualified)|(modified)|(qualified)|(adverse)\s?', re.IGNORECASE)
typecor = {i-1:x for i, x in enumerate(['no opinion/rating', 'unmodified', 'clean', 'unqualified', 'modified', 'qualified', 'adverse'])}

df = df.reindex(columns=df.columns.tolist() + ['text','opinion_freq', 'opinion'])
df[['text', 'opinion','opinion_freq']] = df['dest'].apply(get_text_op, axis=1)

df['has_opinion'] = True
df.loc[df['opinion_freq']==0,'has_opinion'] = False

optype = []

def get_type(matchobj):
    for i, val in enumerate(matchobj.groups()):
        if val is not None:
            return i
    return -1

for x in df['opinion']:
    meron = False
    for item in x:
        res = opinions.match(item)
        if res is not None:
            optype.append(get_type(res))
            meron = True
            break
    if not meron:
        optype.append(-1)

df['op_type'] = optype
df['op_type_text'] = df['op_type'].apply(lambda x: typecor[x])
df.loc[df['is_avail']==False, 'op_type_text'] = 'N/A' # for those whose files are JPG

df.to_csv(P_DIR+'balikbayanbox.csv', encoding='utf-8', index=False)

df = df.drop('text', axis=1)
no_sub = re.compile('(failed to submit|non-submission)|(uncorrected)|(absence)|(accounting errors)|(doubtful)|(unreliable)|(deficienc[yies]+)|(failure)|(unadjusted)|(error[s]?)|(unreconciled)|(omissions)', re.IGNORECASE)
no_types = ['Non-submission*','Uncorrected','Absence','Accounting Errors','Doubtful','Unreliable', 'Deficiency*', 'Failure', 'Unadjusted', 'Errors*', 'Unreconciled', 'Omissions']

no_op = pd.DataFrame(df[df['op_type_text']=='no opinion/rating'][['agency', 'dest']])

buffer = []
for x in no_op['dest']:
    with open(TXT_PATH+x, 'r', encoding='utf-8') as f:
        words = no_sub.findall(f.read())
        if len(words)>=1:
            buffer.append([len(list(filter(lambda el: el!='', x))) for x in list(zip(*words))])

buffer = list(zip(*buffer))
for i, x in enumerate(no_types):
    no_op[x] = buffer[i]
no_op['TOTAL'] = no_op.iloc[:,2:2+len(no_types)].sum(axis=1)
# no_op['(Non-Accounting) Error[s]'] = no_op['(Non-Accounting) Error[s]']-no_op['Accounting Errors'] - produces negative??

ntf_re = re.compile('((\s+(\w+\s)){0,10}(((National Task Force\s+)(\w+\s){2,10})|(NTF[\w\s.-]{2,10})))')
ntf_re2 = re.compile('((National Task Force\s+)(\w+\s){2,10})|(NTF[\w.-]{2,10})')
mga = []
cnt = []
for x in df['dest']:
    with open(TXT_PATH+x, 'r', encoding='utf-8') as f:
        ntf = ntf_re2.findall(f.read())
        mga.append(ntf)
        cnt.append(len(ntf))
df['ntf'] = mga
df['ntf_count'] = cnt
df.to_csv(P_DIR + 'text_analysis.csv', encoding='utf-8')
no_op.to_csv(P_DIR + 'no_ratings.csv', encoding='utf-8') # no_ratings + documents are available
# selector: df[(df['no_op_reason']!='N/A')&(df['is_avail']==True)][['agency','type', 'no_op_reason']]
