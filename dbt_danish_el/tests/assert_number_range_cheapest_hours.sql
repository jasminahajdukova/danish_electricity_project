select price_area, hour, avg_price_by_hour_rank
from {{ref('cheapest_hours')}}
where   (hour not between 0 and 23) or
        (avg_price_by_hour_rank not between 1 and 24)    