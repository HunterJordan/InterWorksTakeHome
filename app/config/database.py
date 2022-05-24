from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import psycopg2
import sqlalchemy.pool as pool
from sqlalchemy.pool import QueuePool
import psycopg2
from sqlalchemy.orm import sessionmaker
from app.schemas.base import Base
from app.utils import notify
import os


def get_db_connection():
    notify('gear', "Setting Up Database!")
    pg_user = os.getenv('DB_USER')
    pg_pass = os.getenv('DB_PASS')
    pg_db = os.getenv('DB_DATABASE')
    pg_host = os.getenv('DB_HOST')
    pg_port = os.getenv('DB_PORT')

    def get_conn():
        keepalive_kwargs = {
            "keepalives": 1,
            "keepalives_idle": 60,
            "keepalives_interval": 10,
            "keepalives_count": 5
        }

        c = psycopg2.connect(

            host=pg_host,
            database=pg_db,
            user=pg_user,
            password=pg_pass,
            port=pg_port,
            **keepalive_kwargs
        )
        return c

    mypool = pool.QueuePool(get_conn, max_overflow=10, pool_size=5)
    engine = create_engine(
        f'postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}',
        echo=True,
        pool_pre_ping=True,
        poolclass=QueuePool
    )
    notify("gear", "Database Connection Success!")

    # create sqlalchemy session
    session = sessionmaker(bind=engine)
    db = session()

    notify("gear", "Preparing database and creating tables!")

    # get model metadata
    metadata = Base.metadata

    # drop all tables with metadata
    for name in metadata.tables.keys():
        engine.execute(f'DROP TABLE IF EXISTS "{name}"')

    # create all tables with metadata
    metadata.create_all(engine)
    notify('praise', "Database prepared!")
    return db
