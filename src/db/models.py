from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class FlatScraped(Base):
    __tablename__: str = "scraped_flats"

    id = Column(Integer, primary_key=True, nullable=False)
    city = Column(String, nullable=True)
    street = Column(String, nullable=True)
    object_ = Column(String, nullable=True)
    area = Column(String, nullable=True)
    number_of_rooms = Column(String, nullable=True)
    floors = Column(String, nullable=True)
    floor = Column(String, nullable=True)
    price_per_square_m = Column(String, nullable=True)
    total_price = Column(String, nullable=True)
    description = Column(String, nullable=True)
    links_to_img = Column(String, nullable=True)
    build_year = Column(String, nullable=True)
    heating = Column(String, nullable=True)
    furnishment = Column(String, nullable=True)
    building = Column(String, nullable=True)
    operation = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class FlatForPrediction(Base):
    __tablename__: str = "predicted_flats"

    id = Column(Integer, primary_key=True, nullable=False)
    city = Column(String, nullable=True)
    street = Column(String, nullable=True)
    object_ = Column(String, nullable=True)
    area = Column(String, nullable=True)
    number_of_rooms = Column(String, nullable=True)
    floors = Column(String, nullable=True)
    floor = Column(String, nullable=True)
    description = Column(String, nullable=True)
    links_to_img = Column(String, nullable=True)
    build_year = Column(String, nullable=True)
    heating = Column(String, nullable=True)
    furnishment = Column(String, nullable=True)
    building = Column(String, nullable=True)
    operation = Column(String, nullable=True)
    predicted_price = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
