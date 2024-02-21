from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class PlaneModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    airplane_name: str
    num_seats: str
    status: str
    manufacture_date: str