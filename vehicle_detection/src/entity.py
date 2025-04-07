from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from vehicle_detection.config.settings import DATABASE_URL

Base = declarative_base()

class TrafficData(Base):
    __tablename__ = 'traffic_data'
    
    id = Column(Integer, primary_key=True)
    location_name = Column(String(100), nullable=False)
    density = Column(Float, nullable=False)
    vehicle_count = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

class TrafficHistory(Base):
    __tablename__ = 'traffic_history'
    
    id = Column(Integer, primary_key=True)
    location_name = Column(String(100), nullable=False)
    density = Column(Float, nullable=False)
    vehicle_count = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

# Tạo engine và session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()