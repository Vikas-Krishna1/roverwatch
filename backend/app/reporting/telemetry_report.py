
from sqlmodel import Session, select
from sqlalchemy import case, func

from app.database import engine
from ..models.Sensor import Sensor
from ..models.Telemetry import Telemetry


def summarize_sensor_readings(
    sensor_id: int,
    metric: str,
    threshold: float = 280.0,
) -> dict:
    """Summarize stored telemetry and count readings above a threshold."""

    with Session(engine) as session:
        sensor = session.get(Sensor, sensor_id)

        if sensor is None:
            raise ValueError(f"Sensor {sensor_id} does not exist.")

        statement = select(
            func.count(Telemetry.id),
            func.min(Telemetry.value),
            func.max(Telemetry.value),
            func.avg(Telemetry.value),
            func.min(Telemetry.timestamp),
            func.max(Telemetry.timestamp),
            func.sum(
                case(
                    (Telemetry.value > threshold, 1),
                    else_=0,
                )
            ),
        ).where(
            Telemetry.sensor_id == sensor_id,
            Telemetry.metric == metric,
        )

        row = session.exec(statement).one()

        if row[0] == 0:
            raise ValueError(
                f"No readings found for sensor {sensor_id}, "
                f"metric {metric!r}."
            )

        return {
            "sensor_id": sensor_id,
            "sensor_name": sensor.name,
            "metric": metric,
            "count": row[0],
            "minimum": row[1],
            "maximum": row[2],
            "average": row[3],
            "first_timestamp": row[4],
            "last_timestamp": row[5],
            "threshold": threshold,
            "above_threshold_count": row[6] or 0,
        }


if __name__ == "__main__":
    report = summarize_sensor_readings(
        sensor_id=7,
        metric="TB Sensor 1A",
        threshold=280.0,
    )

    print("RoverWatch Telemetry Report")
    print("---------------------------")
    print(f"Sensor: {report['sensor_name']}")
    print(f"Metric: {report['metric']}")
    print(f"Readings: {report['count']}")
    print(f"Minimum: {report['minimum']:.2f} K")
    print(f"Maximum: {report['maximum']:.2f} K")
    print(f"Average: {report['average']:.2f} K")
    print(f"First reading: {report['first_timestamp']}")
    print(f"Last reading: {report['last_timestamp']}")
    print(
        f"Readings above {report['threshold']:.2f} K: "
        f"{report['above_threshold_count']}"
    )
