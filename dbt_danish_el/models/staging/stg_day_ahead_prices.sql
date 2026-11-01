select 
    "TimeUTC"::timestamp AT TIME ZONE 'UTC' AS time_utc,
    "TimeDK"::timestamp AT TIME ZONE 'Europe/Copenhagen' AS time_dk,
    "PriceArea" as price_area,
    "DayAheadPriceEUR" as day_ahead_price_eur,
    "DayAheadPriceDKK" as day_ahead_price_dkk
from {{ source('danish_electricity', 'dayaheadprices') }}