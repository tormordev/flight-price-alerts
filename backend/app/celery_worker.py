from celery import Celery
from celery.utils.log import get_task_logger
import os
import logging
from celery.schedules import crontab
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import FlightNotification, User
from app.database import SessionLocal
from app.email_service import send_email
from amadeus import Client, ResponseError
import re

# Initialize Celery
celery = Celery("worker", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

# Configure logging
LOG_DIR = "app/logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure logs directory exists
file_handler = logging.FileHandler(os.path.join(LOG_DIR, "celery_worker.log"))
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Amadeus API Client
amadeus = Client(
    client_id=os.getenv("AMADEUS_CLIENT_ID"),
    client_secret=os.getenv("AMADEUS_CLIENT_SECRET"),
)

# Celery Beat Schedule
celery.conf.beat_schedule = {
    "check-and-send-notifications-every-minute": {
        "task": "app.celery_worker.check_and_send_notifications",
        "schedule": crontab(minute="*"),  # Every minute
    },
}


@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def check_and_send_notifications(self):
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        notifications = db.query(FlightNotification).filter(
            FlightNotification.is_active == True,
            or_(
                FlightNotification.last_notification.is_(None),
                FlightNotification.last_notification <= now
            )
        ).all()

        # Post-process notifications with Python logic for frequency and unit
        filtered_notifications = [
            n for n in notifications
            if n.last_notification is None or
               (n.last_notification + get_timedelta(n.frequency, n.frequency_unit) <= now)
        ]

        for notification in filtered_notifications:
            try:
                logger.info(f"Processing notification {notification.id}")
                flights = search_flights(
                    origin=notification.origin,
                    destination=notification.destination,
                    departure_date=notification.departure_date,
                    max_price=notification.max_price,
                )
                if flights:
                    user = db.query(User).filter(User.id == notification.user_id).first()
                    if user:
                        email_body = format_email_body(flights)
                        send_email(user.email, "Flight Price Alert", email_body)
                        logger.info(f"Email sent to {user.email} for notification {notification.id}")
                notification.last_notification = now
                db.commit()
            except Exception as e:
                logger.error(f"Error processing notification {notification.id}: {e}")
                db.rollback()
    except Exception as e:
        logger.error(f"Task failed: {e}")
        raise self.retry(exc=e)
    finally:
        db.close()


def search_flights(origin, destination, departure_date, max_price):
    """
    Calls Amadeus API to search for flights.
    """
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            maxPrice=int(max_price) if max_price else None,
            adults=1  # 1 adult for simplicity
        )
        return response.data  # List of flight offers
    except ResponseError as e:
        logger.error(f"Amadeus API error: {str(e)}")
        return []


def format_email_body(flights):
    """
    Formats flight details into a readable email body, presenting the cheapest and shortest duration flights.
    """
    if not flights:
        return "No flights found matching your criteria."
    logger.info(f"Format email body")

    # Sort flights by price (cheapest first) and duration (shortest first)
    cheapest_flights = sorted(flights, key=lambda f: float(f["price"]["total"]))[:5]
    shortest_flights = sorted(flights, key=lambda f: sum(
        int(segment["duration"].replace("PT", "").replace("H", "").replace("M", ""))
        for segment in f["itineraries"][0]["segments"]
    ))[:5]

    email_body = "Here are the flights matching your criteria:\n\n"

    # Add cheapest flights
    email_body += "Cheapest Flights:\n"
    for flight in cheapest_flights:
        origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        destination = flight["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
        departure_time = flight["itineraries"][0]["segments"][0]["departure"]["at"]
        duration = flight["itineraries"][0]["duration"]
        price = flight["price"]["total"]
        currency = flight["price"]["currency"]
        booking_link = flight.get("meta", {}).get("links", {}).get("self", "No link available")

        email_body += (
            f"From: {origin} to {destination}\n"
            f"Departure: {departure_time}\n"
            f"Duration: {format_duration(duration)}\n"
            f"Price: {price} {currency}\n"
            f"Book here: {booking_link}\n"
            f"{'-' * 40}\n"
        )


    # Add shortest duration flights
    email_body += "Shortest Duration Flights:\n"
    for flight in shortest_flights:
        origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        destination = flight["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
        departure_time = flight["itineraries"][0]["segments"][0]["departure"]["at"]
        duration = flight["itineraries"][0]["duration"]
        price = flight["price"]["total"]
        currency = flight["price"]["currency"]
        booking_link = flight.get("meta", {}).get("links", {}).get("self", "No link available")

        email_body += (
            f"From: {origin} to {destination}\n"
            f"Departure: {departure_time}\n"
            f"Duration: {format_duration(duration)}\n"
            f"Price: {price} {currency}\n"
            f"Book here: {booking_link}\n"
            f"{'-' * 40}\n"
        )

    return email_body


def get_timedelta(frequency, unit):
    """
    Converts frequency and unit to a timedelta object.
    """
    unit_mapping = {
        "minutes": timedelta(minutes=frequency),
        "hours": timedelta(hours=frequency),
        "days": timedelta(days=frequency),
        "weeks": timedelta(weeks=frequency),
    }
    if unit not in unit_mapping:
        raise ValueError(f"Invalid frequency unit: {unit}")
    return unit_mapping[unit]


def format_duration(duration_iso):
    logger.info(f"Format Duration")
    # Extraer horas y minutos usando expresiones regulares
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?", duration_iso)
    if not match:
        return "Unknown duration"
    
    hours = match.group(1) or "0"
    minutes = match.group(2) or "0"
    return f"{int(hours)}h {int(minutes)}m"

