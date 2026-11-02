with hourly_avg as (
    select  price_area, 
            date_part('hour', time_utc AT TIME ZONE 'Europe/Copenhagen') as hour, 
            round(avg(day_ahead_price_eur)::numeric, 2) as avg_price
    from {{ ref('stg_day_ahead_prices') }}
    group by price_area, date_part('hour', time_utc AT TIME ZONE 'Europe/Copenhagen') 
)
select  price_area,
        hour,
        avg_price,
        rank() over (partition by price_area order by avg_price asc) as avg_price_by_hour_rank
from hourly_avg

