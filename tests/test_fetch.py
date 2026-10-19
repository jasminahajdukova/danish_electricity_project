import pytest
import ingestion.fetch as fetch
import pandas as pd
import urllib3
import time

request_calls = []
sleep_calls   = []


class FakeResponse:

    def __init__(self, status, data):
        self.status = status
        self.data   = data

    def json(self):
        return self.data

def fake_sleep(seconds):
    sleep_calls.append(seconds)

def fake_request_404(self, method, url, **kwargs):
    return FakeResponse(404, {})

def fake_request_500(self, method, url, **kwargs):
    request_calls.append(url)
    return FakeResponse(500, {})

def fake_request_200(self, method, url, **kwargs):
    return FakeResponse(200, {
        'total': 576, 
        'filters': '', 
        'dataset': 'DayAheadPrices', 
        'records': 
            [{'TimeUTC': '2026-10-10T21:45:00', 
              'TimeDK': '2026-10-10T23:45:00', 
              'PriceArea': 'DE', 
              'DayAheadPriceEUR': 114.220001, 
              'DayAheadPriceDKK': 853.805929},

              {'TimeUTC': '2026-10-10T21:45:00', 
               'TimeDK': '2026-10-10T23:45:00', 
               'PriceArea': 'DK1', 
               'DayAheadPriceEUR': 112.769997, 
               'DayAheadPriceDKK': 842.967005}]
        }
    )

def test_404_no_retry(monkeypatch):
    monkeypatch.setattr(urllib3.PoolManager, "request", fake_request_404)

    with pytest.raises(RuntimeError, match="404"):
        fetch.get_records_from_dataset("DayAheadPrices", '2026-10-10', '2026-10-11')


def test_500_retry(monkeypatch):
    request_calls.clear()
    sleep_calls.clear()

    max_retries = 5

    monkeypatch.setattr(urllib3.PoolManager, "request", fake_request_500)
    monkeypatch.setattr(time, "sleep", fake_sleep)

    with pytest.raises(RuntimeError, match="Request Unsuccessful after"):
            fetch.get_records_from_dataset(dataset_name="DayAheadPrices", start='2026-10-10', end='2026-10-11', max_retries=max_retries)

    assert len(sleep_calls) == max_retries - 1
    assert len(request_calls) == max_retries


def test_200_success(monkeypatch):
    monkeypatch.setattr(urllib3.PoolManager, "request", fake_request_200)

    df = fetch.get_records_from_dataset("DayAheadPrices", '2026-10-10', '2026-10-11')

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df["PriceArea"]) == ["DE", "DK1"]
    assert df.loc[0, "DayAheadPriceEUR"] == 114.220001
    assert df.loc[1, "PriceArea"] == "DK1"

