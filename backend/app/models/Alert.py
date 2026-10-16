from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Alert(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    severity: str = Field(max_length=20)
    message: str = Field(max_length=500)
    telemetry_id: int = Field( foreign_key="telemetry.id")