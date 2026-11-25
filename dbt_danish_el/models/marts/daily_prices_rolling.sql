select  price_area,
        day_type,
        date,
        avg_price,
        round(avg(avg_price) over (
            partition by price_area
            order by date asc 
            rows between 6 preceding and current row
        ), 2) as moving_avg_7d
from {{ ref('daily_prices') }}
