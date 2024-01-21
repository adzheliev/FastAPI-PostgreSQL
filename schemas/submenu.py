"""Schemas for Submenu create and update requests"""

from pydantic import BaseModel


class SubmenuCreate(BaseModel):
    """Class for Submenu creation with relative fields"""
    title: str
    description: str


class SubmenuUpdate(BaseModel):
    """Class for Submenu update with relative fields"""
    title: str
    description: str
