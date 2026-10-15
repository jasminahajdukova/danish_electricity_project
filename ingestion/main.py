import fetch, load

dataset     = 'dayaheadprices'
start       = '2026-10-10'
end         = '2026-10-11'
table_name  = 'day_ahead_prices'

dataframe = fetch.get_records_from_dataset(dataset_name=dataset, start=start, end=end)
print(dataframe.head())

engine = load.get_engine()
load.create_raw(engine=engine)
result = load.dataframe_to_table(df=dataframe, dataset_name=table_name, engine=engine)
