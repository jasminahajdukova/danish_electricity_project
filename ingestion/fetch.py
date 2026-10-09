import requests


def get_records_from_dataset(dataset_name, start, end):
    url = f'https://api.energidataservice.dk/dataset/{dataset_name}'

    
    response = requests.get(url, params= {"start": start, "end": end})
    response.raise_for_status()
    json_response = response.json()
    total = json_response.get("total", "")
    print(f"Total records found: {total} for daataset name {dataset_name}")



    
get_records_from_dataset("DayAheadPrices", "2026-10-09", "2026-10-10")


