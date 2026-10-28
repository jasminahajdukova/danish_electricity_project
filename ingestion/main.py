import fetch, load
import argparse
from datetime import datetime

def check_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date: {date_str}. Must strictly follow YYYY-MM-DD format.")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch day-ahead prices and CO2 emissions data"
    )

    parser.add_argument(
        "--start",
        type=check_date,
        required=True, 
        help="start date (YYYY-MM-DD, Danish time, inclusive)")
    
    parser.add_argument(
        "--end",
        type=check_date,
        required=True,
        help="end date (YYYY-MM-DD, Danish time, exclusive)")

    args    = parser.parse_args()
    start   = args.start
    end     = args.end

    if start >= end:
        parser.error(f"--start ({start}) cannot be later or on the same date than --end ({end})")

    dataframe_dayaheadprices = fetch.get_records_from_dataset(
        dataset_name="DayAheadPrices",
        start=start, 
        end=end)
    
    dataframe_co2emis = fetch.get_records_from_dataset(
        dataset_name="CO2Emis",
        start=start, 
        end=end)

    engine = load.get_engine()
    load.create_raw(engine=engine)


    result_dayaheadprices = load.load_to_table(df=dataframe_dayaheadprices, 
                                               engine=engine, 
                                               dataset_name="dayaheadprices", 
                                               time='TimeUTC')


    result_co2emis = load.load_to_table(df=dataframe_co2emis,
                                        engine=engine,
                                        dataset_name='co2emis',
                                        time='Minutes5UTC')
   
    return result_dayaheadprices, result_co2emis


if __name__ == "__main__":
    main()