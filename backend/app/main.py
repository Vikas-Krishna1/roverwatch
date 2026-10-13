from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session
from .Telemetry import Telemetry
from .rover import Rover
from .Component import Component
from .Sensor import Sensor
from .Alert import Alert
from .ThresholdRule import ThresholdRule
from .sensorDataMapping import SensorDataMapping
from .DataSource import DataSource

app = FastAPI(title="RoverWatch API")

DATABASE_URL = "sqlite:///roverwatch.db"

engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)
sensor = Sensor(
    name="Motor Temperature Sensor",
    sensor_type="temperature"
)

with Session(engine) as session:
    session.add(sensor)
    session.commit()
    session.refresh(sensor)

print(f"Created sensor with ID: {sensor.id}")

telemetry = Telemetry(
    metric="motor_temperature",
    value=72.5,
    unit="degC"
)

readings = [
    Telemetry(
        metric="motor_temperature",
        value=72.5,
        unit="degC",
        sensor_id=sensor.id
    ),
    Telemetry(
        metric="motor_temperature",
        value=75.0,
        unit="degC",
        sensor_id=sensor.id
    ),
    Telemetry(
        metric="motor_temperature",
        value=78.2,
        unit="degC",
        sensor_id=sensor.id
    )
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