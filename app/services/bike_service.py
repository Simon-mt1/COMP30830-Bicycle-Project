import requests
import env

class BikeService:
    @staticmethod
    def getJCDecauxData():
        try:
            response = requests.get(env.JCDECAUX["URL"], 
                                    params={"apiKey": env.JCDECAUX["API_KEY"], 
                                            "contract": env.JCDECAUX["CONTRACT"]})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching bike data: {e}")
            return None