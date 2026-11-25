with dk1 as (
    select           
        date,
        avg_price as     avg_price_dk1,
        moving_avg_7d as moving_avg_7d_dk1
    from {{ ref('daily_prices_rolling') }}
    where price_area = 'DK1'
),           

dk2 as (
    select           
        date,
        avg_price as     avg_price_dk2,
        moving_avg_7d as moving_avg_7d_dk2
    from {{ ref('daily_prices_rolling') }}
    where price_area = 'DK2'
)  

select
    dk1.date                                        as date,
    dk1.avg_price_dk1                               as avg_price_dk1,
    dk2.avg_price_dk2                               as avg_price_dk2,
    dk1.moving_avg_7d_dk1                           as moving_avg_7d_dk1,
    dk2.moving_avg_7d_dk2                           as moving_avg_7d_dk2,
    (dk1.avg_price_dk1 - dk2.avg_price_dk2)         as dk1_minus_dk2_avg_price,
    (dk1.moving_avg_7d_dk1 - dk2.moving_avg_7d_dk2) as dk1_minus_dk2_moving_avg
from dk1
inner join dk2 on dk1.date = dk2.date
