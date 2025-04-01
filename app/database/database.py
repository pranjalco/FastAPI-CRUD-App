from sqlmodel import SQLModel, create_engine

# URL example: -- postgresql://user:password@hostname/dbname?sslmode=require
NEON_POSTGRES_URL = "Paste your Neon Postgres connection string here"
engine = create_engine(f"postgresql+psycopg2://{NEON_POSTGRES_URL}", connect_args={"sslmode": "require"})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
