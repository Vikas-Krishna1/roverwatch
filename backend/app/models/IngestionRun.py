from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class IngestionRun(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    source_url: str
    accepted_count: int = Field(default=0)
    rejected_count: int = Field(default=0)
    skipped_count: int = Field(default=0)
    status: str = Field(default="running")
