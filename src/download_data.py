from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://guest:ctu-relational@relational.fel.cvut.cz:3306/financial')
out = Path('data/raw')
out.mkdir(parents=True, exist_ok=True)

for t in ['account', 'client', 'disp', 'district', 'card', 'loan', 'order', 'trans']:
    df = pd.read_sql(f'SELECT * FROM `{t}`', engine)
    df.to_csv(out / f'{t}.csv', index=False)
    print(t, df.shape)