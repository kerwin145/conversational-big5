import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the dataset

df = pd.read_csv("Train_final.csv")

# The 5 personality traits
columns_to_check = ['cOPN', 'cCON', 'cEXT', 'cAGR', 'cNEU']

# Initialize a list to store combinations
combinations = []

# Iterate through each row 
for _, row in df[columns_to_check].iterrows():
    combination = tuple(row) # Create a tuple of the y and n
    combinations.append(combination) # Append the combination

# Count the frequency of each combination
combination_counts = Counter(combinations)

# Create a DataFrame
combinations_df = pd.DataFrame(combination_counts.items(), columns=['Combination', 'Count'])

# Prepare data and statistical values for graph elements
combinations_df['Combination'] = combinations_df['Combination'].apply(lambda x: str(x))

mean_count = combinations_df['Count'].mean()
std_dev_count = combinations_df['Count'].std()

norm = plt.Normalize(combinations_df['Count'].min(), combinations_df['Count'].max())
colors = plt.cm.viridis(norm(combinations_df['Count']))

# Plot the graph
plt.figure(figsize=(10, 6))
plt.bar(combinations_df['Combination'], combinations_df['Count'], color=colors)
plt.xticks(rotation=90)
plt.xlabel('Combinations of y and n')
plt.ylabel('Frequency')
plt.title('Frequency of Each Combination of y and n')
plt.figtext(0.15, 0.85, f'Mean: {mean_count:.2f}', fontsize=12, color='black')
plt.figtext(0.15, 0.80, f'Standard Deviation: {std_dev_count:.2f}', fontsize=12, color='black')
plt.tight_layout()
plt.show()

print(f"Mean Frequency: {mean_count:.2f}")
print(f"Standard Deviation of Frequencies: {std_dev_count:.2f}")
