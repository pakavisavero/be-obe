from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv('.env')
SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ.get("DB_USERNAME"),
    os.environ.get("DB_PASSWORD"),
    os.environ.get("DB_HOST"),
    os.environ.get("DB_PORT"),
    os.environ.get("DB_DATABASE"),
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(bind=engine)
