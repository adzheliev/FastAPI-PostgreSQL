"""Schemas for Dish create and update requests"""

from pydantic import BaseModel


class DishCreate(BaseModel):
    """Class for Dish creation with relative fields"""
    title: str
    description: str
    price: str


class DishUpdate(BaseModel):
    """Class for Dish update with relative fields"""
    title: str
    description: str
    price: str
