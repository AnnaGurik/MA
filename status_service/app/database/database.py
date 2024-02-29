from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

URL = 'postgresql://postgres:password@db/Gurk'

engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Plane(Base):
    __tablename__ = 'planes_annagurik'

    id = Column(Integer, primary_key=True, index=True)
    airplane_name = Column(String, nullable=False)
    num_seats = Column(Integer, nullable=False)
    status = Column(String, default="created", nullable=False)
    manufacture_date = Column(DateTime, default=datetime.now(), nullable=False)
