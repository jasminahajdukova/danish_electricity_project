select count(*)
from {{ ref('cleanest_prices_comparison') }}
having count(*) != 96