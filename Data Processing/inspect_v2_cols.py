import pandas as pd
df = pd.read_csv('data/laptops_cleaned_v2.csv')
for col in df.columns:
    print(col)
