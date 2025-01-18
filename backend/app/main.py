from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from .schemas import LocationSearchRequest, FlightSearchRequest
from .auth.routes import router as auth_router
from amadeus import Client, ResponseError
from fastapi.responses import JSONResponse
from typing import List
from .notification_routes import router as notification_router
from .auth.dependencies import get_current_user

# Load environment variables from .env file
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# Configure logging
LOG_DIR = "app/logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure logs directory exists
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "backend.log"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load the allowed origins from the environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
origins = [

]

logger.info(f"Allowed Origins: {allowed_origins}")

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the authentication routes from auth module
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(notification_router, prefix="/notify", tags=["notify"])

# Optional: Add a basic route for testing
@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to FastAPI!"}

# Initialize Amadeus client with credentials from environment variables
amadeus = Client(
    client_id=os.getenv("AMADEUS_CLIENT_ID"),
    client_secret=os.getenv("AMADEUS_CLIENT_SECRET"),
)

@app.post("/api/search_location")
async def search_location(request: LocationSearchRequest, current_user: str = Depends(get_current_user)):
    try:
        logger.info(f"Search location request: {request.keyword}")
        response = amadeus.reference_data.locations.get(
            keyword=request.keyword,
            subType="AIRPORT",
        )
        return {"data": response.data}
    except ResponseError as error:
        logger.error(f"Failed to fetch locations: {error}")
        raise HTTPException(status_code=500, detail="Failed to fetch locations from Amadeus API")

@app.post("/api/flight_destinations")
async def flight_destinations(request: FlightSearchRequest, current_user: str = Depends(get_current_user)):
    try:
        logger.info(f"Received flight destinations request: {request.dict()}")
        params = {
            "origin": request.origin,
            "departureDate": request.departureDate,
            "oneWay": request.oneWay,
            "maxPrice": request.maxPrice,
            "viewBy": request.viewBy,
        }
        if request.duration:
            params["duration"] = request.duration
        if request.nonStop:
            params["nonStop"] = request.nonStop

        logger.info(f"Sending parameters to Amadeus: {params}")
        response = amadeus.shopping.flight_destinations.get(**params)
        return {"data": response.data}
    except ResponseError as error:
        logger.error(f"Amadeus API error: {error}")
        raise HTTPException(status_code=500, detail="Failed to fetch flight destinations from Amadeus API")

@app.get("/api/airport_autocomplete")
async def airport_autocomplete(term: str = Query(...), current_user: str = Depends(get_current_user)):
    try:
        logger.info(f"Autocomplete request for term: {term}")
        response = amadeus.reference_data.locations.get(
            keyword=term,
            subType="AIRPORT,CITY",
        )
        data = [
            {
                "iataCode": location["iataCode"],
                "name": location["name"],
                "cityName": location.get("address", {}).get("cityName", ""),
            }
            for location in response.data
        ]
        return JSONResponse(content=data)
    except ResponseError as error:
        logger.error(f"Autocomplete error: {error}")
        return JSONResponse(content={"error": str(error)}, status_code=500)
