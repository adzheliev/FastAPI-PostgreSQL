import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from utils.database import Base


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True)
    title = Column(String, unique=True)
    description = Column(String)
    submenus = relationship('Submenu', back_populates='menu', cascade='all, delete')