import requests


url = 'https://api.energidataservice.dk/dataset/DayAheadPrices'

response = requests.get(url, params= {"start": "2026-05-05", "end": "2026-05-10", "limit":"5"})


print(response.text)
