from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .Telemetry import Telemetry
from .rover import Rover
from .Component import Component
from .Sensor import Sensor
from .Alert import Alert
from .ThresholdRule import ThresholdRule, ThresholdRuleCreate
from .sensor_data_mapping import SensorDataMapping
from .DataSource import DataSource
from .IngestionRun import IngestionRun
from .RejectedRecord import RejectedRecord
from fastapi import Query, HTTPException
from sqlalchemy import func
from sqlmodel import Session, select
from .telemetry_report import summarize_sensor_readings
from .setup_nasa_source import setup_nasa_source
from .ingestion_service import ingest_nasa_rad_data

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
#___________________________Telemetry Data Management________________________
@app.get("/telemetry", response_model=list[Telemetry])
def read_telemetry(
    sensor_id: int | None = None,
    limit: int = Query(default=50, ge=1, le=100),
):
    with Session(engine) as session:
        statement = select(Telemetry)

        if sensor_id is not None:
            statement = statement.where(
                Telemetry.sensor_id == sensor_id
            )

        statement = statement.order_by(
            Telemetry.timestamp.desc()
        ).limit(limit)

        return session.exec(statement).all()
#GET /telemetry/summary: Retrieves a summary of telemetry data.
@app.get("/telemetry/summary")
def telemetry_summary():
    with Session(engine) as session:
        statement = (
            select(
                Telemetry.sensor_id,
                Telemetry.metric,
                Telemetry.unit,
                func.count().label("reading_count"),
                func.min(Telemetry.value).label("minimum"),
                func.max(Telemetry.value).label("maximum"),
                func.avg(Telemetry.value).label("average"),
            )
            .group_by(
                Telemetry.sensor_id,
                Telemetry.metric,
                Telemetry.unit,
            )
            .order_by(Telemetry.sensor_id)
        )

        rows = session.exec(statement).all()

        return {
            "summaries": [
                {
                    "sensor_id": sensor_id,
                    "metric": metric,
                    "unit": unit,
                    "reading_count": reading_count,
                    "minimum": minimum,
                    "maximum": maximum,
                    "average": average,
                }
                for (
                    sensor_id,
                    metric,
                    unit,
                    reading_count,
                    minimum,
                    maximum,
                    average,
                ) in rows
            ]
        }
@app.get("/telemetry/report")
def telemetry_report(
    sensor_id: int,
    metric: str,
    threshold: float = 280.0,
):
    try:
        report = summarize_sensor_readings(
            sensor_id=sensor_id,
            metric=metric,
            threshold=threshold,
        )
        return report

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
##GET endpoint to retrieve a specific telemetry record by its ID.
@app.get("/telemetry/{telemetry_id}", response_model=Telemetry)
def read_one_telemetry(telemetry_id: int):
    with Session(engine) as session:
        telemetry = session.get(Telemetry, telemetry_id)

        if telemetry is None:
            raise HTTPException(
                status_code=404,
                detail="Telemetry record not found",
            )

        return telemetry
#Get telemetry report for a specific sensor and metric, including the count of readings above a specified threshold.

##_______________________SENSOR READINGS SUMMARY________________________
##GET /sensors: Retrieves a list of all sensors in the database.
@app.get("/sensors")
def read_sensors():
    with Session(engine) as session:
        statement = select(Sensor)
        return session.exec(statement).all()
##GET /sensors/summary: Provides a summary of sensor readings 
# for a specific sensor and metric, including the 
# count of readings above a specified threshold.
@app.get("/sensors/summary")
def summarize_sensor_readings(
    sensor_id: int,
    metric: str,
    threshold: float = 280.0,
):
   with Session(engine) as session:
    statement = (
        select(func.count())
        .select_from(Telemetry)
        .where(
            Telemetry.sensor_id == sensor_id,
            Telemetry.metric == metric,
            Telemetry.value >= threshold,
        )
    )

    reading_count = session.exec(statement).one()

    return {
        "sensor_id": sensor_id,
        "metric": metric,
        "threshold": threshold,
        "comparison": "greater_than_or_equal",
        "reading_count": reading_count,
    }
#Get one specific sensor by its ID-> gets its deails from the database 
# and returns it as a response.
@app.get("/sensors/{sensor_id}", response_model=Sensor)
def read_one_sensor(sensor_id: int):
    with Session(engine) as session:
        sensor = session.get(Sensor, sensor_id)

        if sensor is None:
            raise HTTPException(
                status_code=404,
                detail="Sensor not found",
            )

        return sensor


##_____-_________________________INGESTION RUNS________________________
#GET /ingestion/runs/{run_id}: Retrieves the details 
# of a specific ingestion run by its ID.
@app.post("/ingestion/nasa")
def run_nasa_ingestion():
    setup_nasa_source()
    run_id = ingest_nasa_rad_data()

    return {
        "message": "NASA ingestion completed",
        "run_id": run_id,
    }
#GET /ingestion/runs/{run_id}: Retrieves the details 
# of a specific ingestion run by its ID.
@app.get("/ingestion/runs")
def read_ingestion_runs(
    limit: int = Query(default=10, ge=1, le=100),
):
    with Session(engine) as session:
        statement = (
            select(IngestionRun)
            .order_by(IngestionRun.id.desc())
            .limit(limit)
        )
        return session.exec(statement).all()
##Get ingestion run by id
@app.get("/ingestion/runs/{run_id}", response_model=IngestionRun)
def read_one_ingestion_run(run_id: int):
    with Session(engine) as session:
        run = session.get(IngestionRun, run_id)

        if run is None:
            raise HTTPException(
                status_code=404,
                detail="Ingestion run not found",
            )

        return run
##GET /ingestion/runs/{run_id}/rejected: Retrieves the rejected records
# for a specific ingestion run by its ID.
@app.get("/ingestion/runs/{run_id}/rejected")
def read_rejected_records(run_id: int):
    with Session(engine) as session:
        statement = select(RejectedRecord).where(
            RejectedRecord.ingestion_run_id == run_id
        )
        return session.exec(statement).all()   
##_________________________Monitoring and Alerts________________________
##GET /threshold-rules — inspect configured thresholds.
@app.get("/threshold-rules")
def read_threshold_rules():
    with Session(engine) as session:
        statement = select(ThresholdRule)
        return session.exec(statement).all()
#Get All alerts from the database
@app.get("/alerts")
def read_alerts():
    with Session(engine) as session:
        statement = select(Alert)
        return session.exec(statement).all()
#Get alert by id from the database
@app.get("/alerts/{alert_id}", response_model=Alert)
def read_one_alert(alert_id: int):
    with Session(engine) as session:
        alert = session.get(Alert, alert_id)

        if alert is None:
            raise HTTPException(
                status_code=404,
                detail="Alert not found",
            )

        return alert
##__________________________Telemetry Report________________________

#___________________________Rover and Component Management________________________
##GET /rovers: Retrieves a list of all rovers in the database.
@app.get("/rovers")
def read_rovers():
    with Session(engine) as session:
        statement = select(Rover)
        return session.exec(statement).all()
#Get one specific rover by its ID-> gets its deails from the database 
# and returns it as a response.
@app.get("/rovers/{rover_id}", response_model=Rover)
def read_one_rover(rover_id: int):
    with Session(engine) as session:
        rover = session.get(Rover, rover_id)

        if rover is None:
            raise HTTPException(
                status_code=404,
                detail="Rover not found",
            )

        return rover
#Get all components from the database
@app.get("/components")
def read_components():
    with Session(engine) as session:
        statement = select(Component)
        return session.exec(statement).all()
@app.get("/components/{component_id}", response_model=Component)
def read_one_component(component_id: int):
    with Session(engine) as session:
        component = session.get(Component, component_id)

        if component is None:
            raise HTTPException(
                status_code=404,
                detail="Component not found",
            )

        return component
@app.post("/threshold-rules", response_model=ThresholdRule)
def create_threshold_rule(rule: ThresholdRuleCreate):
    with Session(engine) as session:
        sensor = session.get(Sensor, rule.sensor_id)

        if sensor is None:
            raise HTTPException(
                status_code=404,
                detail="Sensor not found",
            )

        if rule.warning_limit >= rule.critical_limit:
            raise HTTPException(
                status_code=422,
                detail="warning_limit must be less than critical_limit",
            )

        db_rule = ThresholdRule.model_validate(rule)

        session.add(db_rule)
        session.commit()
        session.refresh(db_rule)

        return db_rule
