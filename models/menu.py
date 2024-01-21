import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from utils.database import Base


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True)
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    submenus = relationship('Submenu', back_populates='menu', cascade='all, delete')
    submenus_count = Column(Integer)
    dishes_count = Column(Integer)
