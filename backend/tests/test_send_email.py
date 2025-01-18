import pytest
from app.email_service import send_email

def test_send_email_success():
    response = send_email("verified_email@example.com", "Test Subject", "<p>Test Content</p>")
    assert response["status_code"] == 202
    assert response["message"] == "Email sent successfully"

def test_send_email_failure():
    response = send_email("invalid_email", "Test Subject", "<p>Test Content</p>")
    assert "error" in response
    assert response["error"] != ""