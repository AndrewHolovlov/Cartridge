from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_USER, DB_PASSWORD, DB_NAME


engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
