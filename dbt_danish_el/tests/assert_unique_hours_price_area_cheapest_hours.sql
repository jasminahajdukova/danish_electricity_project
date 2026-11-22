select price_area, day_type, hour, count(*)
from {{ref('cheapest_hours')}}
group by price_area, day_type, hour
having count(*) > 1