import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database import Base


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    title = Column(String, unique=True)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(UUID, ForeignKey('submenus.id'))
    submenu = relationship('Submenu', back_populates='dishes')
