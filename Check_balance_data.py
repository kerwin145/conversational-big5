import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Replace this with the correct file path
file_path = "Train_final.csv"  # Ensure the file is in the correct location or provide the full path

# Load the CSV file into a DataFrame
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()

# Specify the columns to analyze
columns_to_check = ['cOPN', 'cCON', 'cEXT', 'cAGR', 'cNEU']

# Create a list to store the combinations
combinations = []

# Iterate through each row and form the combination of values from the specified columns
for _, row in df[columns_to_check].iterrows():
    combination = tuple(row)  # Create a tuple of the row values
    combinations.append(combination)

# Count the number of occurrences of each combination
combination_counts = Counter(combinations)

# Convert the combination counts to a DataFrame for easier plotting
combinations_df = pd.DataFrame(combination_counts.items(), columns=['Combination', 'Count'])

# Convert the combinations (tuples) to strings for plotting
combinations_df['Combination'] = combinations_df['Combination'].apply(lambda x: str(x))

# Calculate the mean and standard deviation of the counts
mean_count = combinations_df['Count'].mean()
std_dev_count = combinations_df['Count'].std()

# Normalize the count values to apply colormap
norm = plt.Normalize(combinations_df['Count'].min(), combinations_df['Count'].max())
colors = plt.cm.viridis(norm(combinations_df['Count']))

# Plot with the viridis colormap
plt.figure(figsize=(10, 6))
plt.bar(combinations_df['Combination'], combinations_df['Count'], color=colors)
plt.xticks(rotation=90)
plt.xlabel('Combinations of y and n')
plt.ylabel('Frequency')
plt.title('Frequency of Each Combination of y and n')

# Display the mean and standard deviation as text on the plot
plt.figtext(0.15, 0.85, f'Mean: {mean_count:.2f}', fontsize=12, color='black')
plt.figtext(0.15, 0.80, f'Standard Deviation: {std_dev_count:.2f}', fontsize=12, color='black')

# Show the plot
plt.tight_layout()
plt.show()

# Print the statistics
print(f"Mean Frequency: {mean_count:.2f}")
print(f"Standard Deviation of Frequencies: {std_dev_count:.2f}")
