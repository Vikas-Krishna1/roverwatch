from sqlmodel import Session, select
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from app.database import engine
from app.IngestionRun import IngestionRun
from app.RejectedRecord import RejectedRecord
from app.Sensor import Sensor
from app.DataSource import DataSource
from app.sensor_data_mapping import SensorDataMapping
from app.Telemetry import Telemetry as DBTelemetry
from app.alert_service import evaluate_telemetry
from app.telemetry_processor import (
    fetch_rad_data,
    parse_rad_row,
)


NASA_URL = (
    "https://pds-geosciences.wustl.edu/insight/"
    "urn-nasa-pds-insight_rad/data_calibrated/"
    "hp3_rad_cal_00746_20210101_072936.tab"
)
def mark_run_failed(run_id: int) -> None:
    """Mark an ingestion run as failed."""
    with Session(engine) as session:
        run = session.get(IngestionRun, run_id)

        if run is not None:
            run.status = "failed"
            session.add(run)
            session.commit()


def ingest_nasa_rad_data() -> int:
    """Download, validate, and persist NASA InSight temperature readings."""

    # Create a record before attempting the download.
    with Session(engine) as session:
        run = IngestionRun(source_url=NASA_URL, status="running")
        session.add(run)
        session.commit()
        session.refresh(run)
        run_id = run.id

    print(f"Started ingestion run {run_id}")

    try:
        data = fetch_rad_data()

        with Session(engine) as session:
            sensor = session.exec(
                select(Sensor).where(
                    Sensor.name == "InSight TB Sensor 1A"
                )
            ).first()

            source = session.exec(
                select(DataSource).where(
                    DataSource.source_url == NASA_URL
                )
            ).first()

            if sensor is None or source is None:
                raise ValueError(
                    "NASA source or sensor setup is missing."
                )

            mapping = session.exec(
                select(SensorDataMapping).where(
                    SensorDataMapping.sensor_id == sensor.id,
                    SensorDataMapping.data_source_id == source.id,
                    SensorDataMapping.source_field == "TB Sensor 1A",
                )
            ).first()

            if mapping is None:
                raise ValueError("NASA sensor mapping is missing.")

            accepted = 0
            rejected = 0
            skipped = 0

            for row_number, raw_row in enumerate(
                data.splitlines(), start=1
            ):
                if not raw_row.strip():
                    continue

                try:
                    reading = parse_rad_row(raw_row)

                    statement = (
                        sqlite_insert(DBTelemetry)
                        .values(
                            timestamp=reading.timestamp,
                            metric=reading.metric,
                            value=reading.value,
                            unit=reading.unit,
                            sensor_id=sensor.id,
                            data_kind="NASA PDS archive",
                        )
                        .on_conflict_do_nothing(
                            index_elements=[
                                "sensor_id",
                                "timestamp",
                                "metric",
                            ]
                        )
                        .returning(DBTelemetry.id)
                    )

                    result = session.execute(statement)
                    telemetry_id = result.scalar_one_or_none()

                    if telemetry_id is not None:
                        accepted += 1

                        telemetry = session.get(
                            DBTelemetry,
                            telemetry_id,
                        )

                        if telemetry is None:
                            raise RuntimeError(
                                f"Inserted telemetry {telemetry_id} "
                                "could not be retrieved."
                            )

                        evaluate_telemetry(telemetry, session)

                    else:
                        skipped += 1

                except (ValueError, TypeError, IndexError) as exc:
                    session.add(
                        RejectedRecord(
                            ingestion_run_id=run_id,
                            source_row_number=row_number,
                            raw_row=raw_row,
                            reason=str(exc)[:500],
                        )
                    )
                    rejected += 1

            run = session.get(IngestionRun, run_id)

            if run is None:
                raise ValueError(
                    f"Ingestion run {run_id} no longer exists."
                )

            run.accepted_count = accepted
            run.rejected_count = rejected
            run.skipped_count = skipped
            run.status = "completed"

            session.add(run)
            session.commit()

    except Exception:
        mark_run_failed(run_id)
        raise

    print(f"Accepted readings: {accepted}")
    print(f"Rejected rows: {rejected}")
    print(f"Skipped readings (duplicates): {skipped}")
    print(f"Completed ingestion run {run_id}")

    return run_id

if __name__ == "__main__":
    ingest_nasa_rad_data()