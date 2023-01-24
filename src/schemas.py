from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class FlatBase(BaseModel):
    city: str
    street: str
    area: str
    floors: Optional[str]
    floor: Optional[str]
    number_of_rooms: str
    description: str
    links_to_img: str
    build_year: Optional[str]
    heating: Optional[str]
    furnishment: Optional[str]
    object_: Optional[str]
    building: Optional[str]
    operation: Optional[str]


class FlatCreate(FlatBase):
    pass