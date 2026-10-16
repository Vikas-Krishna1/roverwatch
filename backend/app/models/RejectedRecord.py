from datetime import datetime, timezone

from sqlmodel import SQLModel, Field


class RejectedRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    ingestion_run_id: int = Field(
        foreign_key="ingestionrun.id"
    )
    source_row_number: int
    raw_row: str
    reason: str = Field(max_length=500)

    rejected_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )