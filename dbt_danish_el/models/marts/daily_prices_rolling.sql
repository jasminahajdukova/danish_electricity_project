with daily_prices_rolling_with_windows as (
    select  
        price_area,
        day_type,
        date,
        avg_price,
        lag(avg_price) over (
            partition by price_area
            order by date asc
        )                                as prev_day_avg_price,
        round(avg(avg_price) over (
            partition by price_area
            order by date asc 
            rows between 6 preceding and current row
        ), 2)                            as moving_avg_7d
    from {{ ref('daily_prices') }}
)

select  *,
        (avg_price - prev_day_avg_price) as avg_price_change_1d
from daily_prices_rolling_with_windows
        