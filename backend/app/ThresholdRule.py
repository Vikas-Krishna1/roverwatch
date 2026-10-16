from sqlmodel import SQLModel, Field


class ThresholdRule(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensor.id")
    warning_limit: float = Field()
    critical_limit: float = Field()
    comparison: str = Field(max_length=10)
class ThresholdRuleCreate(SQLModel):
    sensor_id: int
    warning_limit: float
    critical_limit: float
    comparison: str = Field(max_length=10)