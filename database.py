import pandas as pd
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase

# SQLite connection string pointing to local file
DATABASE_URL = "sqlite:///northwind.db"
engine = create_engine(DATABASE_URL)

def get_db_connection():
    sql_db = SQLDatabase(engine)
    return engine, sql_db

def execute_query(query: str):
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return df