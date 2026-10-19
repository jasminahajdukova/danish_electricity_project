import pytest
from sqlalchemy import text
import ingestion.load as load
import pandas as pd


def test_check_missing_env_variables_success(monkeypatch):
    """Test that check_missing_env_variables passes when all keys exist"""
    monkeypatch.setenv('POSTGRES_DB', 'test_db')
    monkeypatch.setenv('POSTGRES_USER', 'test_user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'test_pass')

    load.check_missing_env_variables()


def test_check_missing_env_variables_fail(monkeypatch):
    """Test that check_missing_env_variables raises RuntimeError when keys are missing"""
    monkeypatch.delenv('POSTGRES_DB', raising=False)
    monkeypatch.setenv('POSTGRES_USER', 'test_user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'test_pass')

    with pytest.raises(RuntimeError, match="POSTGRES_DB missing in .env"):
        load.check_missing_env_variables()


@pytest.fixture
def engine():
    return load.get_engine()

@pytest.fixture
def set_up_engine(engine):
    
    load.create_raw(engine)

    with engine.begin() as conn:
        conn.execute(text(f"DROP table IF EXISTS raw.test_day_ahead_prices"))
        conn.execute(text(f"DROP table IF EXISTS raw.test_co2_emis"))

    yield engine

    with engine.begin() as conn:   
        conn.execute(text(f"DROP table IF EXISTS raw.test_day_ahead_prices"))
        conn.execute(text(f"DROP table IF EXISTS raw.test_co2_emis"))



def test_dayaheadprices_to_table_empty(set_up_engine):
    """Test that passing an empty dataframe returns 0 and does nothing"""
    df            = pd.DataFrame()
    rows_inserted = load.dayaheadprices_to_table(df=df, engine=set_up_engine)
    assert rows_inserted == 0 


def test_dayaheadprices_to_table_inserts_and_handles_overlaps(set_up_engine):
    """Test inserting data and verifying that overlapping records get deleted and replaced"""

    dataset_name = "test_day_ahead_prices"
    
    df1 = pd.DataFrame({
        "TimeUTC": ["2026-06-01T00:00:00", "2026-06-01T01:00:00"],
        "PriceArea": ["DK2", "DK1"],
        "DayAheadPriceEUR": [100.0, 110.0]
    })

    

    load.dayaheadprices_to_table(df=df1, engine=set_up_engine, dataset_name=dataset_name)

    with set_up_engine.connect() as conn:
        total_count = conn.execute(text(f"SELECT count(*) FROM raw.{dataset_name}")).scalar()
        assert total_count == 2


    df2 = pd.DataFrame({
        "TimeUTC": ["2026-06-01T01:00:00", "2026-06-01T02:00:00"],
        "PriceArea": ["DK1", "DK2"],
        "DayAheadPriceEUR": [125.0, 111.1]
    })



    load.dayaheadprices_to_table(df=df2, engine=set_up_engine, dataset_name=dataset_name)

    with set_up_engine.connect() as conn:
            total_count = conn.execute(text(f"SELECT count(*) FROM raw.{dataset_name}")).scalar()
            assert total_count == 3

            updated_price = conn.execute(text(f"select \"DayAheadPriceEUR\" from raw.{dataset_name} where \"TimeUTC\" = :time and  \"PriceArea\" = :price_area"),
                                         {"time": "2026-06-01T01:00:00", "price_area": "DK1"}).scalar()

            assert updated_price == 125.0


def test_co2emis_to_table_empty(set_up_engine):
    "Test that passing and empty dataframe returns 0 and does nothing"
    df                  = pd.DataFrame()
    rows_inserted       = load.co2emis_to_table(df=df, engine=set_up_engine)
    assert rows_inserted==0



def test_co2emis_to_table_inserts_and_handles_overlaps(set_up_engine):
    """Test inserting data and verifying that overlapping records get deleted and replaced"""

    dataset_name = "test_co2_emis"
    
    df1 = pd.DataFrame({
        "Minutes5UTC": ["2026-06-01T00:00:00", "2026-06-01T01:00:00"],
        "PriceArea": ["DK2", "DK1"],
        "CO2Emission": [100.0, 110.0]
    })

    

    load.co2emis_to_table(df=df1, engine=set_up_engine, dataset_name=dataset_name)

    with set_up_engine.connect() as conn:
        total_count = conn.execute(text(f"SELECT count(*) FROM raw.{dataset_name}")).scalar()
        assert total_count == 2


    df2 = pd.DataFrame({
        "Minutes5UTC": ["2026-06-01T01:00:00", "2026-06-01T02:00:00"],
        "PriceArea": ["DK1", "DK2"],
        "CO2Emission": [125.0, 111.1]
    })



    load.co2emis_to_table(df=df2, engine=set_up_engine, dataset_name=dataset_name)

    with set_up_engine.connect() as conn:
            total_count = conn.execute(text(f"SELECT count(*) FROM raw.{dataset_name}")).scalar()
            assert total_count == 3

            updated_price = conn.execute(text(f"select \"CO2Emission\" from raw.{dataset_name} where \"Minutes5UTC\" = :time and  \"PriceArea\" = :price_area"),
                                         {"time": "2026-06-01T01:00:00", "price_area": "DK1"}).scalar()

            assert updated_price == 125.0
