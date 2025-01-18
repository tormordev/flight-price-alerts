import pytest
from fastapi.testclient import TestClient
from app.main import app  # Assuming 'app' is your FastAPI instance
from app.database import get_db
from app.models import FlightNotification
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.auth.dependencies import get_current_user
from unittest.mock import Mock

# Set up a test database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use an SQLite in-memory database for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override for getting the test database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency override for mocking user authentication
def override_get_current_user():
    # Mock a user, assuming `get_current_user` is a function returning the current user
    return Mock(id=1, username="testuser")

# Create the test client with dependency overrides
@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app)
    yield client

# Create the database tables for testing
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Create all tables
    FlightNotification.metadata.create_all(bind=engine)
    yield
    # Clean up: drop tables after tests
    FlightNotification.metadata.drop_all(bind=engine)

def test_create_notification(client):
    # Prepare the data for the new notification
    data = {
        "origin": "MAD",
        "destination": "LPA",
        "departure_date": "2025-02-19",
        "max_price": 69.89,
        "frequency": 2,
        "frequency_unit": "hours",
    }

    response = client.post("/notify/notify/notifications/", json=data)

    assert response.status_code == 200
    notification = response.json()

    # Assert frequency and frequency_unit values
    assert notification["frequency"] == 2
    assert notification["frequency_unit"] == "hours"

    # Assert other fields
    assert notification["origin"] == "MAD"
    assert notification["destination"] == "LPA"
    assert notification["departure_date"] == "2025-02-19"
    assert notification["max_price"] == 69.89
    assert notification["id"] == 1

def test_list_notifications(client):
    # Assuming the notification was created in the previous test
    response = client.get("/notify/notify/notifications/")

    assert response.status_code == 200
    notifications = response.json()
    assert isinstance(notifications, list)  # The response should be a list

def test_delete_notification(client):
    # Assuming a notification with ID 1 exists
    response = client.delete("/notify/notify/notifications/1/")

    assert response.status_code == 200
    assert response.json() == {"message": "Notification deleted successfully"}

    # Verify that the notification was deleted
    response = client.get("/notify/notify/notifications/")
    notifications = response.json()
    assert all(notification["id"] != 1 for notification in notifications)

def test_create_notification_missing_fields(client):
    # Missing required fields
    data = {
        "origin": "MAD",
        "destination": "LPA"
    }

    response = client.post("/notify/notify/notifications/", json=data)
    assert response.status_code == 422  # Unprocessable Entity



def test_delete_nonexistent_notification(client):
    # Attempt to delete a notification that does not exist
    response = client.delete("/notify/notify/notifications/999/")
    assert response.status_code == 404  # Not Found
    assert response.json() == {"detail": "Notification not found"}

def test_create_and_delete_notification(client):
    # Create a notification
    data = {
        "origin": "MAD",
        "destination": "LPA",
        "departure_date": "2025-02-19",
        "max_price": 69.89,
        "frequency": 2,
        "frequency_unit": "hours"
    }
    response = client.post("/notify/notify/notifications/", json=data)
    assert response.status_code == 200
    notification = response.json()
    notification_id = notification["id"]

    # Delete the created notification
    response = client.delete(f"/notify/notify/notifications/{notification_id}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Notification deleted successfully"}

    # Verify that the notification was deleted
    response = client.get("/notify/notify/notifications/")
    notifications = response.json()
    assert all(notification["id"] != notification_id for notification in notifications)
