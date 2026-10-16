from datetime import datetime, timezone

from sqlmodel import SQLModel, Session, create_engine, select
from app.models.ThresholdRule import ThresholdRule
from app.models.Component import Component
from app.models.Sensor import Sensor
from app.models.rover import Rover
from app.models.Alert import Alert
from app.models.Sensor import Sensor
from app.models.Telemetry import Telemetry
from app.models.ThresholdRule import ThresholdRule
from app.services.alert_service import evaluate_telemetry


# Isolated, temporary in-memory database.
test_engine = create_engine("sqlite://")

SQLModel.metadata.create_all(test_engine)


def run_test():
    with Session(test_engine) as session:
        sensor = Sensor(
            name="Test Temperature Sensor",
            sensor_type="temperature",
        )
        session.add(sensor)
        session.commit()
        session.refresh(sensor)

        rule = ThresholdRule(
            sensor_id=sensor.id,
            warning_limit=280.0,
            critical_limit=290.0,
            comparison="greater",
        )
        session.add(rule)
        session.commit()

        scenarios = [
            (275.0, None),
            (285.0, "warning"),
            (295.0, "critical"),
        ]

        for value, expected_severity in scenarios:
            telemetry = Telemetry(
                timestamp=datetime.now(timezone.utc),
                metric="test_temperature",
                value=value,
                unit="K",
                sensor_id=sensor.id,
                data_kind="test",
            )
            session.add(telemetry)
            session.commit()
            session.refresh(telemetry)

            alert = evaluate_telemetry(telemetry, session)

            actual_severity = (
                alert.severity if alert is not None else None
            )

            assert actual_severity == expected_severity, (
                f"{value} K: expected {expected_severity}, "
                f"got {actual_severity}"
            )

            print(
                f"PASS: {value} K -> "
                f"{actual_severity or 'no alert'}"
            )

            # Evaluating the same reading again must not add
            # a second alert for that telemetry ID.
            evaluate_telemetry(telemetry, session)

        alerts = session.exec(select(Alert)).all()

        assert len(alerts) == 2, (
            f"Expected 2 alerts, found {len(alerts)}"
        )

        print("PASS: repeated evaluation created no duplicate alerts.")
        print("All alert scenarios passed.")


if __name__ == "__main__":
    run_test()