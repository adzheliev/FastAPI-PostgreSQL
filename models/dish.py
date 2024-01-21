import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.database import Base


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True)
    title = Column(String, unique=True)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(String, ForeignKey('submenus.id'))
    submenu = relationship('Submenu', back_populates='dishes')