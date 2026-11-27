with co2 as (
    select
        price_area,
        CASE
            when date_part('isodow', minutes_5_utc AT TIME ZONE 'Europe/Copenhagen') in (6,7) then 'weekend'
            else 'weekday'
        END                                                                        as day_type,
        date_part('hour', minutes_5_utc AT TIME ZONE 'Europe/Copenhagen')  as hour,
        avg(co2_emission)::numeric as avg_co2
    from {{ ref('stg_co2_emis') }}
    group by    price_area,
                day_type,
                hour
)

select  price_area,
        day_type,
        hour,
        round(avg_co2, 2)                                                     as avg_co2_emission,
        rank () over (partition by price_area, day_type order by avg_co2 asc) as co2_rank
from co2