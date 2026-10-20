import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()
Base = declarative_base()

class WeatherForecast(Base):
    __tablename__ = 'weather_forecast'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String)
    forecast_date = Column(Date)
    temp_min = Column(Float)
    temp_max = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_session():
    db_url = os.getenv('DB_URL', 'sqlite:///weather_lab.db')
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()