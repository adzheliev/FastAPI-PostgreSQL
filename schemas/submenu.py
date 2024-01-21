from pydantic import BaseModel


class SubmenuCreate(BaseModel):
    title: str
    description: str


class SubmenuUpdate(BaseModel):
    title: str
    description: str