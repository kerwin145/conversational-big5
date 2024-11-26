import pandas as pd

df = pd.read_csv("Train_final.csv")

columns_to_check = ['cOPN', 'cCON', 'cEXT', 'cAGR', 'cNEU']

counts = {col: {'y': 0, 'n': 0} for col in columns_to_check}

for col in columns_to_check:
    if col in df.columns:
        counts[col]['y'] = (df[col] == 'y').sum()
        counts[col]['n'] = (df[col] == 'n').sum()

for col, count in counts.items():
    print(f"{col}: y = {count['y']}, n = {count['n']}")

