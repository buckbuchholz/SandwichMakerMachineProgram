from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from api.dependencies.config import conf
from urllib.parse import quote_plus

# Initial connection without specifying a database
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.user}:{quote_plus(conf.password)}@{conf.host}:{conf.port}/"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
connection = engine.connect()

# Create the database if it doesn't exist
connection.execute(text("CREATE DATABASE IF NOT EXISTS sandwich_maker_api"))
connection.close()

# Reconnect with the specified database
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.user}:{quote_plus(conf.password)}@{conf.host}:{conf.port}/sandwich_maker_api?charset=utf8mb4"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
