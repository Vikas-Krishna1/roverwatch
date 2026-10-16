from sqlmodel import Session, select

from app.database import engine
from app.models.Telemetry import Telemetry
from app.models.Alert import Alert
from app.services.alert_service import evaluate_telemetry


with Session(engine) as session:
    # Find a saved NASA telemetry reading for sensor 7.
    statement = (
        select(Telemetry)
        .where(Telemetry.sensor_id == 7)
        .limit(1)
    )
    telemetry = session.exec(statement).first()

    if telemetry is None:
        print("No telemetry found for sensor 7.")
    else:
        print("Testing reading:")
        print("ID:", telemetry.id)
        print("Metric:", telemetry.metric)
        print("Value:", telemetry.value, telemetry.unit)

        alert = evaluate_telemetry(telemetry, session)

        if alert is None:
            print("No alert generated.")
        else:
            print("Alert generated!")
            print("Severity:", alert.severity)
            print("Message:", alert.message)
            print("Alert ID:", alert.id)