from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    farmer_id = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    mobile = Column(String(15), unique=True, nullable=False, index=True)
    aadhar_number = Column(String(12), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    state = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    village = Column(String(100), nullable=True)
    land_size_acres = Column(Float, nullable=True)
    primary_crops = Column(Text, nullable=True)  # JSON string of crops
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(farmer_id={self.farmer_id}, name={self.full_name})>"
