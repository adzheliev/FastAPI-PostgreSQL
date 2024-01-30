"""Model for Menu entity"""

import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database import Base


class Menu(Base):
    """Class for Menu entity with relative fields"""
    __tablename__ = 'menus'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    title = Column(String, unique=True)
    description = Column(String)
    submenus = relationship(
        'Submenu',
        back_populates='menu',
        cascade='all, delete'
    )
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)

