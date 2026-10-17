from app.ingestion.telemetry_processor import (
    Telemetry,
    fetch_rad_data,
    parse_rad_data,
)
import time
from typing import Iterator
from app.services.alert_service import evaluate_telemetry
from app.models.Sensor import Sensor
from app.models.Telemetry import Telemetry as DBTelemetry
from sqlmodel import Session, select
from app.database import engine
from app.models.sensor_data_mapping import SensorDataMapping
def load_nasa_replay() -> list[Telemetry]:
    data = fetch_rad_data()
    return parse_rad_data(data)
def replay_readings() -> Iterator[Telemetry]:
    readings = load_nasa_replay()
    for reading in readings:
        yield reading
def process_replay_reading(reading: Telemetry) -> DBTelemetry:
    with Session(engine) as session:
        mapping = session.exec(
            select(SensorDataMapping).where(
                SensorDataMapping.source_field == reading.metric
            )
        ).first()

        if mapping is None or mapping.sensor_id is None:
            raise ValueError(
                f"No sensor mapping found for {reading.metric}"
            )

        return DBTelemetry(
            timestamp=reading.timestamp,
            metric=reading.metric,
            value=reading.value,
            unit=reading.unit,
            sensor_id=mapping.sensor_id,
            data_kind="NASA Replay",
        )
def save_replay_reading(reading: DBTelemetry) -> DBTelemetry | None:
    with Session(engine) as session:
        existing = session.exec(
            select(DBTelemetry).where(
                DBTelemetry.sensor_id == reading.sensor_id,
                DBTelemetry.timestamp == reading.timestamp,
                DBTelemetry.metric == reading.metric,
            )
        ).first()

        if existing is not None:
            return None

        session.add(reading)
        session.commit()
        session.refresh(reading)

        evaluate_telemetry(reading, session)

        session.commit()

        return reading
def wait_for_next_reading(
    previous_timestamp,
    current_timestamp,
    speed: float = 1.0,
) -> None:
    elapsed = (
        current_timestamp - previous_timestamp
    ).total_seconds()

    delay = elapsed / speed

    if delay > 0:
        time.sleep(delay)
def run_replay(speed: float = 1.0) -> None:
    previous_timestamp = None

    for reading in replay_readings():
        if previous_timestamp is not None:
            wait_for_next_reading(
                previous_timestamp,
                reading.timestamp,
                speed,
            )

        db_reading = process_replay_reading(reading)
        saved = save_replay_reading(db_reading)

        if saved is not None:
            print(
                f"Replayed: {saved.metric} "
                f"{saved.value} {saved.unit} "
                f"at {saved.timestamp}"
            )
        else:
            print(
                f"Skipped duplicate: "
                f"{reading.metric} "
                f"{reading.value} {reading.unit} "
                f"at {reading.timestamp}"
            )

        previous_timestamp = reading.timestamp
if __name__ == "__main__":
    run_replay()