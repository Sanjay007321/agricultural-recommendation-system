from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    APP_NAME: str = "Crop Management System"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./crop.db"
    
    # JWT Settings
    SECRET_KEY: str = "crop-management-secret-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # State codes for Farmer ID generation (all Indian states and UTs)
    STATE_CODES: dict = {
        "Andhra Pradesh": "AP",
        "Arunachal Pradesh": "AR",
        "Assam": "AS",
        "Bihar": "BR",
        "Chhattisgarh": "CG",
        "Goa": "GA",
        "Gujarat": "GJ",
        "Haryana": "HR",
        "Himachal Pradesh": "HP",
        "Jharkhand": "JH",
        "Karnataka": "KA",
        "Kerala": "KL",
        "Madhya Pradesh": "MP",
        "Maharashtra": "MH",
        "Manipur": "MN",
        "Meghalaya": "ML",
        "Mizoram": "MZ",
        "Nagaland": "NL",
        "Odisha": "OD",
        "Punjab": "PB",
        "Rajasthan": "RJ",
        "Sikkim": "SK",
        "Tamil Nadu": "TN",
        "Telangana": "TS",
        "Tripura": "TR",
        "Uttar Pradesh": "UP",
        "Uttarakhand": "UK",
        "West Bengal": "WB",
        "Delhi": "DL",
        "Jammu and Kashmir": "JK",
        "Ladakh": "LA",
        "Puducherry": "PY",
        "Chandigarh": "CH",
        "Dadra and Nagar Haveli and Daman and Diu": "DN",
        "Lakshadweep": "LD",
        "Andaman and Nicobar Islands": "AN"
    }
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
