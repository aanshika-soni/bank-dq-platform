import pandas as pd

t = pd.read_csv('data/raw/trans.csv', low_memory=False)
print(t['bank'].map(type).value_counts())
print(sorted(t['bank'].dropna().unique()))
x = t[t['account'].notna() & t['bank'].isna()]
print(len(x))
print(x['operation'].fillna('NULL').value_counts())
print(x['k_symbol'].fillna('NULL').value_counts())