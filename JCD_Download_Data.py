import requests
import csv
import os
from datetime import datetime

API_KEY = "9347a60de1bf35e15ebac63cbeb87be30214d8b0"
CONTRACT = "dublin"

# Set the path where CSV files will be saved
SAVE_DIR = "/Users/simon/Desktop/COMP30830-Bicycle-Project/JCDdata"

def get_jcdecaux_data(api_key, contract):
    """
    Fetches the station data for the specified contract (e.g., 'dublin').
    Returns the data as a list of dictionaries.
    """
    url = f"https://api.jcdecaux.com/vls/v1/stations?contract={contract}&apiKey={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_data_to_csv(data, filename):
    """Saves the data to a CSV file."""
    if data:
        # Define the CSV headers based on keys from the first dictionary
        headers = data[0].keys()
        
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

def main():
    # 1. Get Dublin bikes data
    data = get_jcdecaux_data(API_KEY, CONTRACT)

    # 2. Ensure the save directory exists (creates it if missing)
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # 3. Create a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(SAVE_DIR, f"jcdecaux_data_{timestamp}.csv")

    # 4. Save the data to the CSV file
    save_data_to_csv(data, filename)

    print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()
