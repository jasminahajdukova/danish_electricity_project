select price_area, date, count(*)
from {{ref('daily_prices_rolling')}}
group by price_area, date
having count(*) > 1