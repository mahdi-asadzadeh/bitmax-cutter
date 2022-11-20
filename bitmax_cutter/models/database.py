import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bitmax_cutter.core.config import settings
logger = logging.getLogger('uvicorn.error')
engine = create_engine(settings.sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
try:
    logger.info(f'Init Database from address: {settings.sqlalchemy_database_url.host}')
except AttributeError:
    logger.info("Init Database")

def get_conn():
    engine.connect()
    return engine.url.database


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
