from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Column, Integer, String, DateTime

from hackerone import settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

class Deals(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    hid = Column('hid', Integer, unique=True)
    reward = Column('reward', Integer)
    vuln_type = Column('type', String)
    severity = Column('severity', String)
    submission_date = Column('submission_date', DateTime)
    resolved_date = Column('resolved_date', DateTime)
    #link = Column('link', String, nullable=True)
    #location = Column('location', String, nullable=True)
    #time = Column('time', DateTime, nullable=True)
