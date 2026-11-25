from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class EventCreate(BaseModel):
    name: str = Field(min_length = 2, max_length = 100)
    description : str = Field(min_length = 2, max_length = 2000)
    place : str = Field(min_length = 2, max_length = 200)
    datetime: datetime

class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    name: str
    description : str
    place : str
    datetime: datetime