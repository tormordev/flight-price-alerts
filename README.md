TravelBuddy: Your Smart Travel Companion ✈️

Welcome to TravelBuddy, the web app I created because of my passion for traveling and my love for finding the best deals. I’ve noticed that the secret to traveling affordably often lies in adapting to the best prices rather than rigidly sticking to a destination or schedule. That’s why I built this app—to make budget-friendly travel easy and accessible.

Features

    1. Flight Search

    Input your departure airport, budget, and a range of dates (this won’t be the exact dates but a range within which flights can occur). TravelBuddy will present flight options tailored to your criteria, helping you find the most affordable destinations.

    2. Price Notifications

    When viewing a flight, you can subscribe to it. TravelBuddy will monitor prices for flights with the same origin, destination, and travel dates.

    You’ll receive an email notification if the price drops below the current value, ensuring you snag the best deal.

    3. Personalized User Experience

    Account Management: Create an account to save your preferences and notifications.

    Dashboard: Manage your subscriptions for flight alerts directly from your dashboard.

    4. Email Alerts

    Receive real-time notifications about flight price changes, so you don’t have to constantly monitor prices yourself.

    5. Smart Filtering

    Search results are sorted based on affordability and other criteria (e.g., shortest duration), making it easier to pick the best options.

How It Works:

    Search for Flights: Enter your departure airport, date range, and budget to find the most affordable destinations.

    Choose & Subscribe: Select a flight that interests you and subscribe to get price drop notifications.

    Get Notified: TravelBuddy keeps an eye on the flight price for you and sends you an email when a better deal is available.

Motivation

    I built TravelBuddy because I love traveling but hate spending more money than necessary. Many times, the key to affordable travel is flexibility—being willing to adapt to the best deals. I wanted an app that could handle the tedious task of monitoring flight prices and notifying me when opportunities arise, so I could focus on enjoying the journey.

    TravelBuddy is your personal travel assistant, making affordable travel easier and more convenient.

Tech Stack

    Backend: Python, FastAPI, Celery

    Frontend: React

    Database: PostgreSQL

    Messaging: Redis (for Celery task queue and notifications)

    APIs: Amadeus API for flight data, SendGrid for email service

    Email Service: Integrated email notifications for price alerts

    Web Server: Nginx for serving static files and reverse proxying\



"""""" IMPORTANT """"""
    Amadeus API: I initially used the free Amadeus API, which worked well in the beginning. However, I later discovered that it operates in a test environment, which can lead to frequent failures, especially with larger searches or specific date ranges. To ensure reliable results, the Amadeus production API must be used, which requires a paid subscription. Below are some example queries that I know work well, but keep in mind that for full functionality, you will need to switch to Amadeus Production:

        Example Search 1:
        Origin: MAD
        Departure Date: 02/18/2025
        Return Date: 02/19/2025
        Max Price: 70

        Example Search 2:
        Origin: MAD
        Departure Date: 02/18/2025
        Return Date: 02/27/2025
        Max Price: 70
        Duration: 5 days

        Example Search 3:
        Origin: MAD
        Departure Date: 02/18/2025
        One-Way: True
        Max Price: 100

        Example Search 4:
        Origin: LONDON
        Departure Date: 02/19/2025
        Max Price: 60
        One-Way: True

    SendGrid Email Service: Although SendGrid's API often marks email tasks as successful, sometimes the service fails to actually send the emails, despite showing a successful status in Celery logs. This issue can lead to delays or undelivered emails. I recommend considering AWS for email delivery in future iterations of the application.


Getting Started

    Setup Instructions

    Follow these steps to set up and run the project using Docker:

    Clone the repository:

        git clone <repository-url>
        cd flight-price-alerts

    Create a .env file:
        Create a .env file in the root directory based on the provided .env.example file. Ensure all necessary environment variables (API keys, database credentials, etc.) are set correctly.

    Build and start the services:
        Run the following command to build and start the application:

        docker-compose up --build

        Access the application:

        Frontend: Visit http://localhost:3000 to interact with the web app.

        Backend API: Access the FastAPI documentation at http://localhost:8000/docs.


Running Tests:
    Ensure the backend container is running:
        docker-compose up backend
    Run tests inside the backend container:
        docker-compose exec backend pytest
    This will automatically discover and execute all tests in the tests/ folder.


    You may see this fails do too TestClient dont handle cookies correctly
    FAILED tests/test_auth.py::test_login_valid_user - AssertionError: assert 'refresh_token' in <Cookies[]>
    FAILED tests/test_auth.py::test_refresh_token - assert None is not None
    FAILED tests/test_auth.py::test_logout - assert None is not None

Interesting Choices & Lessons Learned:

    Tech Stack: The combination of FastAPI, React, and Celery allowed me to build a highly efficient and scalable application.

    Asynchronous Tasks: Using Celery and Redis for handling notifications ensures the app is responsive and capable of managing multiple tasks.

    Dynamic Search: Implementing flexible flight search options, such as budget and date ranges, adds real value for users seeking affordable travel options.

    User Experience: Integrating email alerts and a dashboard enhances the app's usability.

    Dependence on APIs: Relying on external APIs can be both beneficial and challenging. For example, Amadeus offers a free API in a testing environment. Initially, everything worked well, but I later realized that with larger search queries or specific date ranges, the test environment was unreliable and frequently returned 500 errors. To access full functionality without these issues, upgrading to the production tier is necessary but you have to pay.

    Email Delivery Challenges: While SendGrid offers an API for sending emails, I learned that even when the task is marked as "successful," email delivery can sometimes fail or experience significant delays. This makes it more reliable to use robust services like AWS for critical email notifications.

Future Features:

    Advanced Filters: Add more filters for flight searches, such as airlines, stopovers, or departure times.

    Mobile App: Build a mobile version of TravelBuddy for easier access on the go.

    Multi-Currency Support: Allow users to search and view flight prices in their preferred currency.

TravelBuddy was designed with travelers like you in mind—people who love exploring but don’t want to overspend. It’s flexible, efficient, and helps you focus on making memories instead of worrying about flight prices.

Happy travels! 🌍