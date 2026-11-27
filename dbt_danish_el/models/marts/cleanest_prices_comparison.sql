with cleanest as (
    select
        price_area,
        day_type,
        hour,
        avg_co2_emission,
        co2_rank
    from {{ ref('cleanest_hour') }}
),

prices as (
    select
        price_area,
        day_type,
        hour,
        avg_price,
        cheapest_price_by_hour_rank
    from {{ ref('hourly_prices') }}
)

select
    cleanest.price_area                     as price_area,
    cleanest.day_type                       as day_type,
    cleanest.hour                           as hour,
    cleanest.avg_co2_emission               as avg_co2_emission,
    prices.avg_price                        as avg_price,
    cleanest.co2_rank                       as co2_rank,
    prices.cheapest_price_by_hour_rank      as cheapest_price_by_hour_rank,
    (cleanest.co2_rank - prices.cheapest_price_by_hour_rank) as co2_minus_price_rank
from cleanest
inner join prices
    on cleanest.price_area = prices.price_area
    and cleanest.day_type = prices.day_type
    and cleanest.hour = prices.hour