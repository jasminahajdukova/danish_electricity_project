import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect


load_dotenv()

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER     = os.getenv('POSTGRES_USER')
POSTGRES_DB       = os.getenv('POSTGRES_DB')
POSTGRES_HOST     = "localhost"
POSTGRES_PORT     = os.getenv('POSTGRES_PORT')

def check_missing_env_variables():
    missing = []
    for env_variable in ['POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_PORT']:
        
        if not os.environ.get(env_variable, "").strip():
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


def load_to_table(df, engine, dataset_name, time):

    if df.empty:
            return 0
    
    price_areas = df['PriceArea'].unique().tolist()
    min_time    = df[time].min()
    max_time    = df[time].max()

    with engine.begin() as conn:
        inspector = inspect(conn)
        if inspector.has_table(dataset_name, schema="raw"):
            delete_query = text(f"""
                delete from raw.{dataset_name}
                where "{time}" between :start and :end
                    and "PriceArea" = ANY(:price_areas)
            """)
            conn.execute(delete_query, {"start": min_time, "end": max_time, "price_areas": price_areas})

        return df.to_sql(
            name=dataset_name, 
            con=conn, 
            schema='raw', 
            index=False, 
            if_exists='append')