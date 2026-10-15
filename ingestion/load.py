import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas

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
    engine = create_engine(url)
    return engine

def dataframe_to_table(df, dataset_name, engine):
    return df.to_sql(name=dataset_name, con=engine)


def create_raw(engine):
    with engine.begin() as conn:
        conn.execute(text('CREATE SCHEMA IF NOT EXISTS raw;'))

if __name__ == "__main__":
    try:
        engine = get_engine()
        create_raw(engine=engine)
    except Exception as err:
        print(f"Connection to the {POSTGRES_HOST} for user {POSTGRES_USER} could not be made due to the following error:\n{err}")
