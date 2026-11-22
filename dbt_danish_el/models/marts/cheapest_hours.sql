with hourly_avg as (
    select  price_area, 
            CASE
                when date_part('isodow', time_utc AT TIME ZONE 'Europe/Copenhagen') in (6,7) then 'weekend'
                else 'weekday'
            END                                                             as day_type,
            date_part('hour', time_utc AT TIME ZONE 'Europe/Copenhagen')    as hour, 
            round(avg(day_ahead_price_eur)::numeric, 2)                     as avg_price
    from {{ ref('stg_day_ahead_prices') }}
    group by    price_area,
                day_type,
                hour
)
select  price_area,
        day_type,
        hour,
        avg_price,
        rank() over (partition by price_area, day_type order by avg_price asc) as avg_price_by_hour_rank
from hourly_avg

