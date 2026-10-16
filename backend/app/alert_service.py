from sqlmodel import Session, select

from .Telemetry import Telemetry
from .ThresholdRule import ThresholdRule
from .Alert import Alert


def evaluate_telemetry(
    telemetry: Telemetry,
    session: Session,
) -> Alert | None:
    if telemetry.id is None:
        raise ValueError("Telemetry must be saved before evaluation")
    existing_alert = session.exec(
        select(Alert).where(
            Alert.telemetry_id == telemetry.id
        )
    ).first()

    if existing_alert is not None:
        return existing_alert

    statement = select(ThresholdRule).where(
        ThresholdRule.sensor_id == telemetry.sensor_id
    )
    rule = session.exec(statement).first()

    if rule is None:
        return None

    value = telemetry.value

    if rule.comparison == "greater":
        if value >= rule.critical_limit:
            severity = "critical"
            limit = rule.critical_limit
        elif value >= rule.warning_limit:
            severity = "warning"
            limit = rule.warning_limit
        else:
            return None

    else:
        raise ValueError(
            f"Unsupported comparison: {rule.comparison}"
        )

    alert = Alert(
        severity=severity,
        message=(
            f"{telemetry.metric} reading {value} {telemetry.unit} "
            f"crossed the {severity} threshold of {limit} "
            f"{telemetry.unit} for sensor {telemetry.sensor_id}."
        ),
        telemetry_id=telemetry.id,
    )

    session.add(alert)
    session.flush()

    return alert