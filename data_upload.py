import csv
import os
from pymongo import MongoClient

# MongoDB connection details
MONGO_URI = "mongodb+srv://jimmy:nhantruong@cluster0.2h9tu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "myDatabase"
BASE_PATH = "EEET2574_Assignment2_data"  # Base path containing all CSV files

def extract_metadata_from_filename(filename):
    parts = filename.split('_')
    company_name = parts[0]
    year = parts[-1].split('.')[0]  # Extract year and remove extension
    return company_name, year

def load_csv_to_mongodb(base_path, mongo_uri, database_name):
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        # Drop the database if it already exists
        if database_name in client.list_database_names():
            client.drop_database(database_name)
            print(f"Dropped the existing '{database_name}' database.")

        db = client[database_name]

        for root, _, files in os.walk(base_path):
            for file_name in files:
                if file_name.endswith('.csv'):
                    file_path = os.path.join(root, file_name)
                    company_name, year = extract_metadata_from_filename(file_name)

                    # Determine collection based on file path
                    if "Electricity" in root:
                        collection_name = "electricity"
                    elif "Gas" in root:
                        collection_name = "gas"
                    else:
                        print(f"Skipping file {file_name} as it does not match any known collection.")
                        continue

                    collection = db[collection_name]

                    # Read data from CSV file
                    with open(file_path, mode='r', encoding='utf-8') as file:
                        reader = csv.DictReader(file)  # Read rows as dictionaries
                        data = []
                        for row in reader:
                            row['company_name'] = company_name
                            row['year'] = year
                            data.append(row)

                    if data:
                        # Insert data into MongoDB
                        result = collection.insert_many(data)
                        print(f"Inserted {len(result.inserted_ids)} documents from {file_name} into the {collection_name} collection.")
                    else:
                        print(f"No data found in the CSV file: {file_name}.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the MongoDB connection
        client.close()

if __name__ == "__main__":
    load_csv_to_mongodb(BASE_PATH, MONGO_URI, DATABASE_NAME)
