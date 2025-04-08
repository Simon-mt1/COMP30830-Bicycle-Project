"""
bike_service.py

Provides functionality to retrieve live bike station data from the JCDecaux API.
"""

import requests
import env

class BikeService:
    """
    Service class for fetching bike station data from the JCDecaux API.
    """

    @staticmethod
    def getJCDecauxData():
        """
        Retrieves JCDecaux bike station data.

        Returns:
            list or None: A list of station data if successful, None if an error occurs.
        """
        try:
            response = requests.get(env.JCDECAUX["URL"], 
                                    params={
                                        "apiKey": env.JCDECAUX["API_KEY"], 
                                        "contract": env.JCDECAUX["CONTRACT"]
                                    })
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching bike data: {e}")
            return None
