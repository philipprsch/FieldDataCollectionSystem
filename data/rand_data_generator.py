import csv

# Data to write into the CSV file
data = [
    ['Name', 'Age', 'City'],
    ['Alice', '30', 'New York'],
    ['Bob', '24', 'Los Angeles'],
    ['Charlie', '29', 'Chicago']
]

# Create (or replace if it exists) the data.csv file and write to it
file_name = 'data.csv'

# Open the file in 'w' mode to create or overwrite it
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the data into the CSV file
    writer.writerows(data)

print(f'{file_name} has been created or replaced with the new data.')