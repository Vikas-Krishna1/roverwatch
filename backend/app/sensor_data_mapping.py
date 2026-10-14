from sqlmodel import SQLModel, Field

class SensorDataMapping(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: int | None = Field(default=None, foreign_key="sensor.id")
    data_source_id: int | None = Field(default=None, foreign_key="datasource.id")
    source_field: str = Field(max_length=100)
    source_unit: str | None = Field(default=None, max_length=100)
    conversion: str | None = Field(default=None, max_length=100)