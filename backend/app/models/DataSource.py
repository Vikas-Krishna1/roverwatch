from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class DataSource(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    provider: str = Field(max_length=100)
    source_url: str = Field(max_length=400)
    description: str | None = Field(default=None, max_length=500)
    added_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
