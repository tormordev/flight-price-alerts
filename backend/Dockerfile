# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Copy the requirements file into the container
COPY requirements.txt .

# Create directories for logs and static files
RUN mkdir -p /app/logs /app/static /app/media

RUN pip install --no-cache-dir --default-timeout=400 -r requirements.txt


# Install Redis server
RUN apt-get update && apt-get install -y redis-server && apt-get clean

# Copy the application code into the container
COPY . .

# Expose the Redis and application ports
EXPOSE 6379
EXPOSE 8000

# Default command to start Redis and run the application
CMD ["sh", "-c", "redis-server --daemonize yes && cd /app/app && alembic -c alembic.ini upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
