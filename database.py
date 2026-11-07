import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#Read the .env file
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD"))
MYSQL_DB = os.getenv("MYSQL_DB")

#Make the full MySQL connection string
DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}/{MYSQL_DB}"
)

#Engine makes the connection to MySQL
engine = create_engine(DATABASE_URL)

#Session is used to talk to the database (add, read, update, delete)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base is the parent of all our tables (used in models.py)
Base = declarative_base()


#FastAPI will use this function to open and close a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
