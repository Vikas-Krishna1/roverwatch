from datetime import datetime
from sqlmodel import SQLModel, Field
import httpx
RAD_SENSOR_1A_TEMPERATURE_INDEX = 15
class Telemetry(SQLModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metric: str
    value: float
    unit: str

def parse_rad_row(row: str) -> Telemetry:
    fields = row.split()
    if len(fields) != 39:
        raise ValueError(
        f"Expected 39 fields, got {len(fields)}"
    )

    return Telemetry(
        timestamp=datetime.fromisoformat(fields[0]),
        metric="TB Sensor 1A",
        value=float(fields[RAD_SENSOR_1A_TEMPERATURE_INDEX]),
        unit="K",
    )
def fetch_rad_data() -> str:
    url = (
    "https://pds-geosciences.wustl.edu/insight/"
    "urn-nasa-pds-insight_rad/data_calibrated/"
    "hp3_rad_cal_00746_20210101_072936.tab"
)

    response = httpx.get(url, timeout=30.0)
    response.raise_for_status()
    return response.text

def parse_rad_data(data: str) -> list[Telemetry]:
    readings = []

    for row in data.splitlines():
        if not row.strip():
            continue

        readings.append(parse_rad_row(row))

    return readings

def summarize_readings(readings: list[Telemetry]) -> dict:
    values = [reading.value for reading in readings]

    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "average": sum(values) / len(values),
    }


def find_readings_above(
    readings: list[Telemetry],
    threshold: float,
) -> list[Telemetry]:
    return [
        reading
        for reading in readings
        if reading.value > threshold
    ]
