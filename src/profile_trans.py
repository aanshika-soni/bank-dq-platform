import pandas as pd

t = pd.read_csv('data/raw/trans.csv', low_memory=False)
for c in ['type', 'operation', 'k_symbol']:
    print(t[c].value_counts(dropna=False))
    print()
print(t['amount'].describe())
print(t['balance'].describe())
print('Date range:', t['date'].min(), 'to', t['date'].max())
print('Duplicate trans_id:', t['trans_id'].duplicated().sum())