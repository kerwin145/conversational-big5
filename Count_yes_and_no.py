import pandas as pd

# Load the dataset
df1 = pd.read_csv("Train_final.csv")
df2 = pd.read_csv("evaldata.csv")
df3 = pd.read_csv("testdata.csv")
# The 5 personality traits
columns_to_check = ['cOPN', 'cCON', 'cEXT', 'cAGR', 'cNEU']

# Initialize a dictionary
counts = {col: {'y': 0, 'n': 0} for col in columns_to_check}

for dataset in [df1, df2, df3]:
    for col in columns_to_check:
        if col in dataset.columns:
            counts[col]['y'] = (dataset[col] == 'y').sum() #count y
            counts[col]['n'] = (dataset[col] == 'n').sum() #count n

    for col, count in counts.items():
        print(f"{col}: y = {count['y']}, n = {count['n']}")

