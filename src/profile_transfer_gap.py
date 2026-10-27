import pandas as pd

t = pd.read_csv('data/raw/trans.csv', low_memory=False)
tr = t[t['operation'].isin(['PREVOD NA UCET', 'PREVOD Z UCTU'])]
print(tr[tr['bank'].isna() | tr['account'].isna()].to_string())