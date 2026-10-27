import pandas as pd

t = pd.read_csv('data/raw/trans.csv', low_memory=False)
print('Zero amounts:', (t['amount'] == 0).sum())
print('Negative balances:', (t['balance'] < 0).sum())
print('k_symbol blank text:', t['k_symbol'].str.strip().eq('').sum())
print()
print(pd.crosstab(t['operation'].isna(), t['k_symbol'].eq('UROK'),
                  rownames=['operation is null'], colnames=['k_symbol is UROK']))
print()
print(pd.crosstab(t['type'], t['operation'].fillna('NULL')))
print()
print('bank filled, account null:', (t['bank'].notna() & t['account'].isna()).sum())
print('account filled, bank null:', (t['bank'].isna() & t['account'].notna()).sum())
o = pd.read_csv('data/raw/order.csv')
print('order k_symbol blank text:', o['k_symbol'].str.strip().eq('').sum())