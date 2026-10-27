import pandas as pd

t = pd.read_csv('data/raw/trans.csv', low_memory=False)
tr = t[t['operation'].isin(['PREVOD NA UCET', 'PREVOD Z UCTU'])]
print('Transfers:', len(tr))
print('Transfers with bank null:', tr['bank'].isna().sum())
print('Transfers with account null:', tr['account'].isna().sum())
print('Non-transfers with bank filled:', t[~t.index.isin(tr.index) & t['bank'].notna()].shape[0])