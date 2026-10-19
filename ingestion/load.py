import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect


load_dotenv()

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER     = os.getenv('POSTGRES_USER')
POSTGRES_DB       = os.getenv('POSTGRES_DB')
POSTGRES_HOST     = "localhost"
POSTGRES_PORT     = '5432'

def check_missing_env_variables():
    missing = []
    for env_variable in ['POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD']:
        if env_variable not in os.environ:
            missing.append(env_variable)

    if missing:
        raise RuntimeError(f"{', '.join(missing)} missing in .env")
def get_engine():
    check_missing_env_variables()
    url = f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    engine = create_engine(url=url)
    return engine


def create_raw(engine):
    with engine.begin() as conn:
        conn.execute(text('CREATE SCHEMA IF NOT EXISTS raw;'))

def dayaheadprices_to_table(df, engine, dataset_name="dayaheadprices"):

    if df.empty:
        return 0

    price_areas = df['PriceArea'].unique().tolist()
    min_time    = df['TimeUTC'].min()
    max_time    = df['TimeUTC'].max()

    with engine.begin() as conn:
        inspector = inspect(conn)
        if inspector.has_table(dataset_name, schema="raw"):
            delete_query = text(f"""
                delete from raw.{dataset_name}
                where "TimeUTC" between :start and :end
                    and "PriceArea" = ANY(:price_areas)
            """)
            conn.execute(delete_query, {"start": min_time, "end": max_time, "price_areas": price_areas})

        return df.to_sql(
            name=dataset_name, 
            con=conn, 
            schema='raw', 
            index=False, 
            if_exists='append')


def co2emis_to_table(df, engine, dataset_name="co2emis"):

    if df.empty:
        return 0

    price_areas = df['PriceArea'].unique().tolist()
    min_time    = df['Minutes5UTC'].min()
    max_time    = df['Minutes5UTC'].max()

    with engine.begin() as conn:
        inspector = inspect(conn)
        if inspector.has_table(dataset_name, schema="raw"):
            delete_query = text(f"""
                delete from raw.{dataset_name}
                where "Minutes5UTC" between :start and :end
                    and "PriceArea" = ANY(:price_areas)
            """)
            conn.execute(delete_query, {"start": min_time, "end": max_time, "price_areas": price_areas})

        return df.to_sql(
            name=dataset_name, 
            con=conn, 
            schema='raw', 
            index=False, 
            if_exists='append')

