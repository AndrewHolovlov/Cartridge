from datetime import datetime
from sqlalchemy.sql import func

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from database.database import Base, engine


class Cartridge(Base):
    __tablename__ = 'cartridges'

    id = Column(Integer, primary_key=True)
    id_cartridge = Column(String(20))
    types = Column(String(50))
    corps = Column(Integer)
    audience = Column(Integer)
    note = Column(Text)
    state = Column(String(20))
    create_at = Column(DateTime, default=func.now())
    last_update = Column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    state = Column(Text, nullable=False)
    create_at = Column(DateTime, default=datetime.now)
    last_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_admin = Column(Boolean, nullable=False)


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
