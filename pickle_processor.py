import pickle
import csv

# Load the pickled dictionary
with open('data/vid data.pickle', 'rb') as pickle_file:
    loaded_dict = pickle.load(pickle_file)

# Create a CSV file for writing
with open('output.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow(['Words', 'Download Links'])

    for key, value in loaded_dict.items():
        print(key)
        writer.writerow([key, value])
