from sqlmodel import SQLModel
from pydantic import BaseModel


# Create pydantic model because we wanted to do data validation
class CreateUser(BaseModel):
    name: str
    email: str
    password: str


# Create a class with the help of which we can exclude the password
class ExcludeInfo(SQLModel):
    id: int
    name: str
    email: str | None























