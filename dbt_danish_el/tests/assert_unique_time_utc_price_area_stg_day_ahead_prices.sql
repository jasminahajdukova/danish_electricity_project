select time_utc, price_area, count(*)
from {{ref('stg_day_ahead_prices')}}
group by time_utc, price_area
having count(*) > 1