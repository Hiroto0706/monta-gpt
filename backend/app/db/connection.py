from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import utilities.config as config

engine = create_engine(config.POSTGRES_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baseクラスを定義
Base = declarative_base()


def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
