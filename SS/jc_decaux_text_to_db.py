import requests
import traceback
import datetime
import time
import os
import dbinfo
import json
import sqlalchemy as sqla
from sqlalchemy import create_engine, text  # Import `text` for SQL queries

def stations_to_db(text, in_engine):
    # Load the stations from the text received from JCDecaux
    stations = json.loads(text)

    # Print type of the stations object and number of stations
    print(type(stations), len(stations))
    
    # Use a database connection
    with in_engine.connect() as connection:
        for station in stations:
            print(type(station))

            # Extract relevant info for insertion
            vals = {
                "address": station.get('address'),
                "banking": int(station.get('banking')),
                "bikestands": int(station.get('bike_stands')),
                "name": station.get('name'),
                "status": station.get('status')
            }

            # Use a parameterized query with SQLAlchemy's `text()` function
            query = text("""
                INSERT INTO station (address, banking, bikestands, name, status) 
                VALUES (:address, :banking, :bikestands, :name, :status);
            """)

            connection.execute(query, vals)  # Execute the query with values

        connection.commit()  # Commit the transaction

def main():
    USER = "root"
    PASSWORD = "Buzz1357"
    PORT = "3306"
    DB = "local_databasejcdecaux"
    URI = "127.0.0.1"

    connection_string = f"mysql+pymysql://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}"

    engine = create_engine(connection_string, echo=True)

    try:
        r = requests.get(dbinfo.STATIONS_URI, params={"apiKey": dbinfo.JCKEY, "contract": dbinfo.NAME})
        stations_to_db(r.text, engine)
        time.sleep(5 * 60)
    except Exception as e:
        print(traceback.format_exc())

# Run the script
main()