select price_area, day_type, hour, count(*)
from {{ref('hourly_prices')}}
group by price_area, day_type, hour
having count(*) > 1