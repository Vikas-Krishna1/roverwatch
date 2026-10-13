from sqlmodel import SQLModel, Field

class Rover(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: str | None = Field(default=None, max_length=50)