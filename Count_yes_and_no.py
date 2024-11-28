import pandas as pd

# Load the dataset
df = pd.read_csv("Train_final.csv")
# The 5 personality traits
columns_to_check = ['cOPN', 'cCON', 'cEXT', 'cAGR', 'cNEU']

# Initialize a dictionary
counts = {col: {'y': 0, 'n': 0} for col in columns_to_check}

for col in columns_to_check:
    if col in df.columns:
        counts[col]['y'] = (df[col] == 'y').sum() #count y
        counts[col]['n'] = (df[col] == 'n').sum() #count n

for col, count in counts.items():
    print(f"{col}: y = {count['y']}, n = {count['n']}")

