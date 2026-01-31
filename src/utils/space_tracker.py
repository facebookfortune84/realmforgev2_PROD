import json
import requests

data = requests.get('https://api.spacexdata.com/v4/launches/latest').json()

launch_name = data['name']
launch_date = data['date_utc']

print(f'Launch Name: {launch_name}')
print(f'Launch Date (UTC): {launch_date}')
