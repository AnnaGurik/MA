from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class PlaneModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    airplane_name: str
    num_seats: int
    status: Optional[str] = None
    manufacture_date: Optional[datetime] = None