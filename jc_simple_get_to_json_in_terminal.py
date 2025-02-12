import requests
import json
import dbinfo

response = requests.get(dbinfo.STATIONS_URI, params={'apiKey': dbinfo.API_KEY, "contract": dbinfo.CONTRACT})

print(response.status_code)  # Check the HTTP status code (200 means success)
print(response.text)  # Print raw response

if response.status_code == 200:
    data = json.loads(response.text)
    print(json.dumps(data, indent=4))
else:
    print(f"Error: {response.status_code}, Message: {response.text}")
