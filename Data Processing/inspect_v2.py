import pandas as pd
df = pd.read_csv('data/laptops_cleaned_v2.csv')
print("Columns:", df.columns.tolist())
print(df.head(2))
