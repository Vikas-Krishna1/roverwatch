from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session

from .Telemetry import Telemetry


app = FastAPI(title="RoverWatch API")

DATABASE_URL = "sqlite:///roverwatch.db"

engine = create_engine(DATABASE_URL)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


telemetry = Telemetry(
    metric="motor_temperature",
    value=72.5,
    unit="degC"
)
readings = [
    Telemetry(metric="motor_temperature", value=72.5, unit="degC"),
    Telemetry(metric="motor_temperature", value=75.0, unit="degC"),
    Telemetry(metric="motor_temperature", value=78.2, unit="degC")
]



with Session(engine) as session:
    session.add_all(readings)
    session.commit()
    print(f"Telemetry readings added to the database: {len(readings)}")


@app.get("/")
def root():
    return {"message": "RoverWatch API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}