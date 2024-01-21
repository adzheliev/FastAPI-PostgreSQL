import uuid
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from utils.database import Base


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True)
    title = Column(String, unique=True)
    description = Column(String)
    menu_id = Column(String, ForeignKey('menus.id'))
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete')
    dishes_count = Column(Integer)