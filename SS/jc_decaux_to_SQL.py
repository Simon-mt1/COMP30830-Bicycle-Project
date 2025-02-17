import requests
import mysql.connector
from mysql.connector import Error

# Replace with your actual values
API_KEY = "9347a60de1bf35e15ebac63cbeb87be30214d8b0"
CONTRACT = "dublin"

DB_HOST = "localhost"
DB_NAME = "dublin_bikes"
DB_USER = "root"
DB_PASSWORD = "Buzz1357"

def get_dublin_bikes_data(api_key, contract):
    """
    Fetches the station data for the specified contract (city).
    Returns the data as a list of dictionaries.
    """
    url = f"https://api.jcdecaux.com/vls/v1/stations?contract={contract}&apiKey={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def insert_station_data(data, connection):
    """
    Inserts or updates station data in the database.
    """
    cursor = connection.cursor()

    # MySQL upsert approach: either do a "REPLACE" or "INSERT ... ON DUPLICATE KEY UPDATE"
    # We'll use "INSERT ... ON DUPLICATE KEY UPDATE"
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
        cursor.execute(sql, data)
        connection.commit()
    except Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        cursor.close()

def main():
    # 1. Download the Dublin bikes data from JCDecaux
    bikes_data = get_dublin_bikes_data(API_KEY, CONTRACT)

    # 2. Connect to the MySQL database
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            print("Successfully connected to the database.")

            # 3. Iterate over each station and insert into the DB
            for station in bikes_data:
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

            print("Data insertion complete.")

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    main()
