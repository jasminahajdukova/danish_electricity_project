select 
    "Minutes5UTC"::timestamp AT TIME ZONE 'UTC' AS minutes_5_utc,
    "PriceArea" as price_area,
    "CO2Emission" as co2_emission
from {{ source('danish_electricity', 'co2emis') }}
