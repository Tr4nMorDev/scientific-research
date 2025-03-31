from sqlalchemy import Column, String, Float
from .base import BaseModel

class Vehicle(BaseModel):
    __tablename__ = "vehicles"

    type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float) 