import os
import json
import mysql.connector
from mysql.connector import Error

# === Replace these with your database details ===
DB_HOST = "localhost"
DB_NAME = "dublin_bikes"
DB_USER = "root"
DB_PASSWORD = "Buzz1357"

# Path to the folder where Script #1 saved the JSON data
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
            %(lat)s,
            %(lng)s,
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

            # 2. Process all JSON files in the DATA_DIR
            for file_name in os.listdir(DATA_DIR):
                if file_name.endswith(".json"):
                    file_path = os.path.join(DATA_DIR, file_name)
                    print(f"Reading data from {file_path}")

                    with open(file_path, "r") as f:
                        stations_list = json.load(f)

                    # 3. Insert/update each station from this file
                    for station in stations_list:
                        station_data = {
                            'number': station.get('number'),
                            'name': station.get('name'),
                            'address': station.get('address'),
                            'lat': station['position'].get('lat'),
                            'lng': station['position'].get('lng'),
                            'banking': 1 if station.get('banking') else 0,
                            'bonus': 1 if station.get('bonus') else 0,
                            'status': station.get('status'),
                            'bike_stands': station.get('bike_stands'),
                            'available_bike_stands': station.get('available_bike_stands'),
                            'available_bikes': station.get('available_bikes'),
                            'last_update': station.get('last_update')
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
