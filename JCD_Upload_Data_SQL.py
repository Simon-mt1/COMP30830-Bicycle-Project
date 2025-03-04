import os
import csv
import mysql.connector
from mysql.connector import Error

DB_HOST = "localhost"
DB_NAME = "dublin_bikes"
DB_USER = "root"
DB_PASSWORD = "Buzz1357"

# Path to the folder where CSV files are saved
DATA_DIR = "/Users/simon/Desktop/COMP30830-Bicycle-Project/JCDdata"

def insert_station_data(station_data, connection):
    """
    Inserts (or updates) one station record into the 'stations' table.
    Uses MySQL's 'ON DUPLICATE KEY UPDATE' for upserting.
    """
    cursor = connection.cursor()
    sql = """
        INSERT INTO stations (
            number,
            name,
            address,
            latitude,
            longitude,
            banking,
            bonus,
            status,
            bike_stands,
            available_bike_stands,
            available_bikes,
            last_update
        )
        VALUES (
            %(number)s,
            %(name)s,
            %(address)s,
            %(latitude)s,
            %(longitude)s,
            %(banking)s,
            %(bonus)s,
            %(status)s,
            %(bike_stands)s,
            %(available_bike_stands)s,
            %(available_bikes)s,
            %(last_update)s
        )
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            address = VALUES(address),
            latitude = VALUES(latitude),
            longitude = VALUES(longitude),
            banking = VALUES(banking),
            bonus = VALUES(bonus),
            status = VALUES(status),
            bike_stands = VALUES(bike_stands),
            available_bike_stands = VALUES(available_bike_stands),
            available_bikes = VALUES(available_bikes),
            last_update = VALUES(last_update);
    """
    try:
        cursor.execute(sql, station_data)
        connection.commit()
    except Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        cursor.close()

def main():
    # 1. Connect to MySQL
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            print("Successfully connected to the database.")

            # 2. Process all CSV files in the DATA_DIR
            for file_name in os.listdir(DATA_DIR):
                if file_name.endswith(".csv"):
                    file_path = os.path.join(DATA_DIR, file_name)
                    print(f"Reading data from {file_path}")

                    with open(file_path, "r", newline="") as f:
                        reader = csv.DictReader(f)

                        # 3. Insert/update each station from this file
                        for row in reader:
                            station_data = {
                                'number': int(row['number']),
                                'name': row['name'],
                                'address': row['address'],
                                'latitude': float(row['latitude']),
                                'longitude': float(row['longitude']),
                                'banking': int(row['banking']),
                                'bonus': int(row['bonus']),
                                'status': row['status'],
                                'bike_stands': int(row['bike_stands']),
                                'available_bike_stands': int(row['available_bike_stands']),
                                'available_bikes': int(row['available_bikes']),
                                'last_update': int(row['last_update'])  # Assuming this is a timestamp
                            }
                            insert_station_data(station_data, connection)

                    print(f"Finished inserting data from {file_path}")

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        # 4. Close the DB connection
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    main()
