from sqlmodel import SQLModel, Field

class Component(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    rover_id: int | None = Field(default=None, foreign_key="rover.id")
    name: str = Field(max_length=100)
    component_type: str = Field(max_length=50)
    description: str | None = Field(default=None, max_length=500)
