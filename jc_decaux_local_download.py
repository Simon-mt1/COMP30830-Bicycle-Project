########## SCRIPT TO DOWNLOAD INFORMATION FROM JCDECAUX LOCALLY ##########

import requests
import traceback
import datetime
import time
import os
import dbinfo

# Will be used to store text in a file
def write_to_file(text):
   
    # I first need to create a folder data where the files will be stored.
    
    if not os.path.exists('JCDdata'):
        os.mkdir('JCDdata')
        print("Folder 'JCDdata' created!")
    else:
        print("Folder 'JCDdata' already exists.")

    # now is a variable from datetime, which will go in {}.
    # replace is replacing white spaces with underscores in the file names
    now = datetime.datetime.now()
    with open("JCDdata/bikes_{}".format(now).replace(" ", "_"), "w") as f:
        f.write(text)

# Empty for now
def write_to_db(text):
    return 0

# Main function to download the data and write it to a file
def main():
    while True:
        try:
            response = requests.get(dbinfo.STATIONS_URI, params={'apiKey': dbinfo.API_KEY, "contract": dbinfo.CONTRACT})
            print(response)
            write_to_file(response.text)
            time.sleep(5*60)
        except:
            print(traceback.format_exc())

# CTRL + Z to stop it
main()    