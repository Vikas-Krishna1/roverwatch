from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class Telemetry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metric: str = Field(max_length=100)
    value: float = Field()
    unit: str = Field(max_length=20)
    sensor_id: int = Field( foreign_key="sensor.id")
    data_kind: str | None = Field(default=None, max_length=50)