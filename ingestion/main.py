import fetch, load

start       = '2026-10-10'
end         = '2026-10-12'


dataframe_dayaheadprices = fetch.get_records_from_dataset(dataset_name="DayAheadPrices",start=start, end=end)
dataframe_co2emis         = fetch.get_records_from_dataset(dataset_name="CO2Emis",start=start, end=end)

print("==================================================================================================================")
print(dataframe_dayaheadprices.head())
print("==================================================================================================================")
print(dataframe_co2emis.head())
print("==================================================================================================================")

engine = load.get_engine()
load.create_raw(engine=engine)
result_dayaheadprices = load.dayaheadprices_to_table(df=dataframe_dayaheadprices, engine=engine)
result_co2emis        = load.co2emis_to_table(df=dataframe_co2emis, engine=engine)