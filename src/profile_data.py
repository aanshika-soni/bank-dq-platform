from pathlib import Path
import pandas as pd

for f in sorted(Path('data/raw').glob('*.csv')):
    df = pd.read_csv(f)
    print('=' * 60)
    print(f.name, df.shape)
    print(df.dtypes)
    nulls = df.isna().sum()
    print('Columns with nulls:')
    print(nulls[nulls > 0])
    print('Duplicate rows:', df.duplicated().sum())
    print(df.head(3))