import csv
import ast

data_dict = {}

with open('CFLBeacon.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data_title = row['Title']
        offset = row['Offset']
        size = row['Size']
        signed = row['Signed']
        conversion_function = row['Conversion Function']

        data_dict[data_title] = {
            "Offset": offset,
            "Size": size,
            "Signed": signed,
            "Conversion function": conversion_function
        }

# Printing the resulting dictionary
for key, value in data_dict.items():
    print(key)
    print(value)


def apply_conversion(expression, X):
    try:
        result = eval(expression, {'X': X})
        return result
    except Exception as e:
        return f"Error: {e}"
