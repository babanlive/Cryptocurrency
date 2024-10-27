from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PriceBase(BaseModel):
    id: int
    ticker: str
    price: float
    timestamp: datetime


class PriceRead(PriceBase):
    model_config: ConfigDict = ConfigDict(from_attributes=True)
    id: int
