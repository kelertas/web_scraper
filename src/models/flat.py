from pydantic import BaseModel
from typing import Optional


class Flat(BaseModel):
    city: str
    street: str
    area: str
    floors: str
    floor: str
    number_of_rooms: str
    price_per_square_m: str
    total_price: str
    description: str
    links_to_img: str
    build_year: Optional[str]
    heating: Optional[str]
    furnishment: Optional[str]
    object_: Optional[str]
    building: Optional[str]
    operation: Optional[str]


class FlatUrl(BaseModel):
    url: str
