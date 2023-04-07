import pandas as pd

# Read your CSV file
data = pd.read_csv("your_input_file.csv")

# Add a unique ID column (you can name it as you want, e.g., 'id')
data.insert(0, "id", data.index + 1)

# Write the modified DataFrame to a new CSV file
data.to_csv("your_output_file.csv", index=False)
