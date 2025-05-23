from sqlalchemy import Column, Integer, String, Float, Date
from .db import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    date = Column(Date, index=True)
    avgtemp_c = Column(Float)
  
