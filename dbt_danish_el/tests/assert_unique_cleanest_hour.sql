select price_area, day_type, hour, count(*)
from {{ref('cleanest_hour')}}
group by price_area, day_type, hour
having count(*) > 1