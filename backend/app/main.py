from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine

from .Telemetry import Telemetry


app = FastAPI(title="RoverWatch API")

DATABASE_URL = "sqlite:///roverwatch.db"

engine = create_engine(DATABASE_URL)
telemetry = Telemetry(metric="motor_temperature", value=72.5, unit="degC")
print(telemetry)
print(telemetry.timestamp)  # This will print the current UTC timestamp


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def root():
    return {"message": "RoverWatch API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}