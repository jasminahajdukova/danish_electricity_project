select price_area, hour, cheapest_price_by_hour_rank
from {{ref('hourly_prices')}}
where   (hour not between 0 and 23) or
        (cheapest_price_by_hour_rank not between 1 and 24)    