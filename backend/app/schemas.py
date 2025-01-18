from pydantic import BaseModel, EmailStr, validator,Field
import re
from typing import Optional 
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 18:
            raise ValueError("Password must be at least 18 characters long")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[@$!%*?&]", value):
            raise ValueError("Password must contain at least one special character")
        return value

class UserResponse(BaseModel):
    message: str
    redirect_url: str

    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class FlightNotificationCreate(BaseModel):
    origin: str
    destination: str
    departure_date: str
    max_price: float
    frequency: int
    frequency_unit: str

class FlightNotificationResponse(BaseModel):
    origin: str
    destination: str
    departure_date: str
    max_price: float
    frequency: int
    frequency_unit: str
    id: int

class FlightSearchRequest(BaseModel):
    origin: str = Field(..., description="IATA code of the city from which the flight will depart")
    departureDate: str = Field(..., description="The date, or range of dates, on which the flight will depart")
    oneWay: Optional[bool] = Field(False, description="If this parameter is set to true, only one-way flights are considered")
    duration: Optional[str] = Field(None, description="Exact duration or range of durations of the travel, in days")
    nonStop: Optional[bool] = Field(False, description="If this parameter is set to true, only non-stop flights are considered")
    maxPrice: Optional[int] = Field(None, ge=0, description="Defines the price limit for each offer returned")
    viewBy: Optional[str] = Field("DURATION", description="View the flight destinations by DATE, DESTINATION, DURATION, WEEK, or COUNTRY")
    
    class Config:
        schema_extra = {
            "example": {
                "origin": "MAD",
                "departureDate": "2025-05-01,2025-05-15",
                "oneWay": False,
                "duration": "3,7",
                "nonStop": True,
                "maxPrice": 500,
                "viewBy": "DURATION"
            }
        }

class LocationSearchRequest(BaseModel):
    keyword: str = Field(..., description="The keyword (e.g., city or airport code) to search for locations")
    
    class Config:
        schema_extra = {
            "example": {
                "keyword": "LON"
            }
        }