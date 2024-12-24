import os
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class WaterLog(Base):
    __tablename__ = 'water_logs'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Database setup
db_path = os.path.expanduser('~/.local/share/driink/driink.db')
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)