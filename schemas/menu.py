"""Schemas for Menu create and update requests"""

from pydantic import BaseModel


class MenuCreate(BaseModel):
    """Class for Menu creation with relative fields"""
    title: str
    description: str


class MenuUpdate(BaseModel):
    """Class for Menu update with relative fields"""
    title: str
    description: str
