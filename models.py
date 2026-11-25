from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Events(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(100), nullable = False)
    description = Column(String(2000), nullable = False)
    place = Column(String(200), nullable = False)
    datetime = Column(DateTime, nullable = False)



