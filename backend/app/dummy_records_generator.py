import random
from datetime import datetime, timedelta
from app.models import FlightDestinationDummy  # Import your model
from app.database import SessionLocal  # Import your session management

# Helper function to generate random data
def generate_dummy_data(db):
    origins = ['MAD', 'LON', 'JFK', 'LAX', 'PAR']
    destinations = ['BCN', 'AMS','MIA', 'SFO', 'ROM']
    today = datetime.today()

    for _ in range(1000):  # Generate 1000 records
        origin = random.choice(origins)
        destination = random.choice(destinations)
        departure_date = today + timedelta(days=random.randint(1, 180))
        price = round(random.uniform(50, 1000), 2)
        max_price = round(random.uniform(50, 2000), 2)
        one_way = random.choice([True, False])
        duration = random.randint(3, 14)  # Random trip duration between 3 and 14 days
        non_stop = random.choice([True, False])
        view_by = 'DURATION'

        # Create a new FlightDestinationDummy instance
        flight = FlightDestinationDummy(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            price=price,
            max_price=max_price,
            one_way=one_way,
            duration=duration,
            non_stop=non_stop,
            view_by=view_by
        )

        # Add the record to the session
        db.add(flight)

    # Commit the transaction to the database
    db.commit()

def main():
    db = SessionLocal()  # Get the database session
    try:
        generate_dummy_data(db)
        print("Dummy data generation complete.")
    finally:
        db.close()  # Make sure to close the session after use

if __name__ == '__main__':
    main()