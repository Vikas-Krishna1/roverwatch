from sqlmodel import Session, select

from app.database import engine
from ..models.DataSource import DataSource
from ..models.Sensor import Sensor
from ..models.sensor_data_mapping import SensorDataMapping
from ..models.Component import Component


NASA_URL = (
    "https://pds-geosciences.wustl.edu/insight/"
    "urn-nasa-pds-insight_rad/data_calibrated/"
    "hp3_rad_cal_00746_20210101_072936.tab"
)


def setup_nasa_source():
    with Session(engine) as session:
        # 1. Register the NASA data source.
        source = session.exec(
            select(DataSource).where(DataSource.source_url == NASA_URL)
        ).first()

        if source is None:
            source = DataSource(
                name="NASA InSight HP3 Radiometer Archive",
                provider="NASA PDS Geosciences",
                source_url=NASA_URL,
                description=(
                    "Archived calibrated InSight radiometer observations "
                    "from January through March 2021."
                ),
            )
            session.add(source)
            session.flush()

        # 2. Register the NASA temperature sensors.
        sensor_names = [
            "InSight TB Sensor 1A",
            "InSight TB Sensor 1B",
            "InSight TB Sensor 1C",
            "InSight TB Sensor 2A",
            "InSight TB Sensor 2B",
            "InSight TB Sensor 2C",
        ]

        sensors = []

        for sensor_name in sensor_names:
            sensor = session.exec(
                select(Sensor).where(
                    Sensor.name == sensor_name
                )
            ).first()

            if sensor is None:
                sensor = Sensor(
                    name=sensor_name,
                    sensor_type="temperature",
                    component_id=None,
                )
                session.add(sensor)
                session.flush()

            sensors.append(sensor)

        # 3. Register the source-field-to-sensor mappings.
        sensor_fields = [
            "TB Sensor 1A",
            "TB Sensor 1B",
            "TB Sensor 1C",
            "TB Sensor 2A",
            "TB Sensor 2B",
            "TB Sensor 2C",
        ]

        for sensor, field in zip(sensors, sensor_fields):
            mapping = session.exec(
                select(SensorDataMapping).where(
                    SensorDataMapping.sensor_id == sensor.id,
                    SensorDataMapping.data_source_id == source.id,
                    SensorDataMapping.source_field == field,
                )
            ).first()

            if mapping is None:
                mapping = SensorDataMapping(
                    sensor_id=sensor.id,
                    data_source_id=source.id,
                    source_field=field,
                    source_unit="K",
                    conversion=None,
                )
                session.add(mapping)
                session.flush()

            print(
                f"Registered mapping: {mapping.source_field} -> "
                f"Sensor ID {mapping.sensor_id}"
            )

        session.commit()

        print("NASA source ID:", source.id)
        print("NASA sensors registered:", len(sensors))


if __name__ == "__main__":
    setup_nasa_source()