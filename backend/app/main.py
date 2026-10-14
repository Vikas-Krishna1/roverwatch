from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .Telemetry import Telemetry
from .rover import Rover
from .Component import Component
from .Sensor import Sensor
from .Alert import Alert
from .ThresholdRule import ThresholdRule
from .sensor_data_mapping import SensorDataMapping
from .DataSource import DataSource

app = FastAPI(title="RoverWatch API")

SQLModel.metadata.create_all(engine)
##Root endpoint- Checks if the API is running and returns a
#  message indicating that the RoverWatch API is operational.
@app.get("/")
def root():
    return {"message": "RoverWatch API is running"}
# HEALTH CHECK ENDPOINT - Checks the health of the API 
# and returns a status indicating whether the API is healthy or not.
@app.get("/health")
def health_check():
    return {"status": "healthy"}
##POST endpoint to create a new rover in the database.
