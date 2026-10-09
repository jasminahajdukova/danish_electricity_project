import requests
import pandas as pd


def get_records_from_dataset(dataset_name, start, end):
    url = f'https://api.energidataservice.dk/dataset/{dataset_name}'

    
    response = requests.get(url, params= {"start": start, "end": end})
    response.raise_for_status()
    json_response = response.json()
    df = pd.DataFrame(json_response["records"])
    return df


if __name__ == "__main__":    
    result = get_records_from_dataset("DayAheadPrices", "2026-10-09", "2026-10-10")
    print("==========================================================================================")
    print(result.shape)
    print("==========================================================================================")
    print(result.head())
    print("==========================================================================================")
    print(result.dtypes)
    print("==========================================================================================")
