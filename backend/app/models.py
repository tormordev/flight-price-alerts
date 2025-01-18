from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Numeric, Date
from .database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    flight_notifications = relationship("FlightNotification", back_populates="user", cascade="all, delete-orphan")
    
class FlightNotification(Base):
    __tablename__ = "flight_notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_date = Column(String, nullable=False)
    max_price = Column(Numeric(10, 2), nullable=True)
    
    # Frequency in number of units (e.g., 1, 2, 3)
    frequency = Column(Integer, nullable=False, default=1)
    
    # Frequency unit (minutes, hours, days, weeks)
    frequency_unit = Column(String, nullable=False, default="days")
    
    is_active = Column(Boolean, default=True)
    last_notification = Column(DateTime, nullable=True)

    # Define the relationship to the user (if needed)
    user = relationship("User", back_populates="flight_notifications")

    @validates('max_price')
    def validate_max_price(self, key, value):
        if value is not None and value < 0:
            raise ValueError("max_price should be a positive value.")
        return value

class FlightDestinationDummy(Base):
    __tablename__ = 'flight_destinations_dummy'
    
    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String(3), nullable=False)  # IATA code
    destination = Column(String(3), nullable=False)  # IATA code
    departure_date = Column(Date, nullable=False)
    price = Column(Numeric(10, 2))
    max_price = Column(Numeric(10, 2))
    one_way = Column(Boolean, default=False)
    duration = Column(Integer)  # Duration in days
    non_stop = Column(Boolean, default=False)
    view_by = Column(String(20), default="DURATION")
    
    @validates('origin', 'destination')
    def validate_iata_code(self, key, value):
        if len(value) != 3:
            raise ValueError(f"{key} should be a valid IATA code.")
        return value

    def __repr__(self):
        return f"<FlightDestination(origin={self.origin}, destination={self.destination}, departure_date={self.departure_date}, price={self.price})>"

