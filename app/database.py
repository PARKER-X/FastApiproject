from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
import time


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database connection postgre but we use sqlachemy
try:
    conn = psycopg2.connect(host="localhost", database='fastapi', user='postgres', password = 'password123', cursor_factory = RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was succesfull!")
except Exception as error:
    print("Failed to connect database")
    print("Error:",error)
    time.sleep(2)
