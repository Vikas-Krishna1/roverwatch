from sqlmodel import SQLModel, Field

class Sensor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    sensor_type: str = Field(max_length=50)
    component_id: int | None = Field(default=None, foreign_key="component.id")