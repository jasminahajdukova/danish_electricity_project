select price_area, hour, count(*)
from {{ref('cheapest_hours')}}
group by price_area, hour
having count(*) > 1