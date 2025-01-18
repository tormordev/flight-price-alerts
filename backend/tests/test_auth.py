import pytest
from fastapi.testclient import TestClient
from app.main import app  # Replace with the actual entry point of your FastAPI app
from datetime import timedelta

client = TestClient(app)

# Mock user credentials
VALID_EMAIL = "test7@test.com"
VALID_PASSWORD = "74£MXy@TM;(TuHJ6La"
INVALID_EMAIL = "invalidexample.com"
INVALID_PASSWORD = "wrongpassword"




def test_register_user():
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={"email": VALID_EMAIL, "password": VALID_PASSWORD, "confirmPassword": VALID_PASSWORD},
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_register_user_existing():
    """Test registering a user with an existing email."""
    response = client.post(
        "/auth/register",
        json={"email": VALID_EMAIL, "password": VALID_PASSWORD, "confirmPassword": VALID_PASSWORD},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email is already registered"


def test_register_user_invalid_email():
    """Test registration with invalid email."""
    response = client.post(
        "/auth/register",
        json={"email": "invalid-email", "password": VALID_PASSWORD, "confirmPassword": VALID_PASSWORD},
    )
    assert response.status_code == 422


def test_login_valid_user():
    """Test login with valid credentials."""
    response = client.post(
        "/auth/login", json={"email": VALID_EMAIL, "password": VALID_PASSWORD}
    )
    print(f"Aqui{response.cookies} and {response.headers}") 
    assert response.status_code == 200
    assert "refresh_token" in response.cookies
    assert "access_token" in response.cookies
    


def test_login_invalid_user():
    """Test login with invalid credentials."""
    response = client.post(
        "/auth/login", json={"email": INVALID_EMAIL, "password": INVALID_PASSWORD}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"


def test_access_protected_route_without_login():
    """Test access to a protected route without login."""
    response = client.get("/auth/home")
    assert response.status_code == 401
    assert response.json()["detail"] == "Access token missing"


def test_access_protected_route_with_invalid_token():
    """Test access to a protected route with an invalid token."""
    client.cookies.set("access_token", "fake.invalid.token")
    response = client.get("/auth/home")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_refresh_token():
    """Test refreshing tokens."""
    login_response = client.post(
        "/auth/login", json={"email": VALID_EMAIL, "password": VALID_PASSWORD}
    )
    refresh_token = login_response.cookies.get("refresh_token")

    assert refresh_token is not None

    client.cookies.set("refresh_token", refresh_token)
    response = client.post("/auth/refresh")
    assert response.status_code == 200
    assert "access_token" in response.cookies


def test_logout():
    """Test logout functionality."""
    login_response = client.post(
        "/auth/login", json={"email": VALID_EMAIL, "password": VALID_PASSWORD}
    )
    access_token = login_response.cookies.get("access_token")
    assert access_token is not None

    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "access_token" not in response.cookies
    assert "refresh_token" not in response.cookies
