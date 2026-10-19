import pandas as pd
import urllib3
import time

def get_records_from_dataset(dataset_name, start, end, max_retries=3):
    http = urllib3.PoolManager()
    api_url = f'https://api.energidataservice.dk/dataset/{dataset_name}'

    for attempt in range(1, max_retries + 1):
        try:
            response = http.request('GET', api_url, fields={"start": start, "end": end})

            if response.status == 200:
                print(f"{dataset_name}: GET Request Successful on attempt {attempt}")
                json_response = response.json()
                df = pd.DataFrame(json_response["records"])
                return df
            elif response.status == 429 or response.status >= 500:
                print(f"{dataset_name}: Attempt {attempt}: Status Code {response.status}. Retrying...")
            else:
                raise RuntimeError(f"{dataset_name}: GET Request Unsuccessful. Status Code {response.status}. Not retrying")
        
        except urllib3.exceptions.RequestError as err:
                print(f"Error: {err}")

        if attempt != max_retries:
                time.sleep(15)

    raise RuntimeError(f"{dataset_name}: GET Request Unsuccessful after {max_retries} attempts")

