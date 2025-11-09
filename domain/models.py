from sqlalchemy import (
    Column, BigInteger, Integer, String, Date, DateTime, Enum
)
from sqlalchemy.sql import func
from database import database_config

class Festival(database_config.Base):
    __tablename__ = "Festival"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    addr1 = Column(String(255), nullable=False)
    addr2 = Column(String(255), nullable=True)
    areaCode = Column(Integer, nullable=False)
    contentId = Column(String(255), nullable=True)

    createdDate = Column(DateTime, server_default=func.now())
    updatedDate = Column(DateTime, onupdate=func.now()) 

    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)

    festivalType = Column(
        Enum("FESTAPICK", "TOUR_API", name="festival_type_enum"), 
        nullable=False
    )
    state = Column(
        Enum("APPROVED", "DENINED", "PROCESSING", name="state_enum"), 
        nullable=False
    )

    homePage = Column(String(500), nullable=True)
    posterInfo = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    overView = Column(String(5000), nullable=False)

    manager_id = Column(BigInteger, nullable=True)
