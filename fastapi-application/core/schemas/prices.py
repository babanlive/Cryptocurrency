from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PriceBase(BaseModel):
    ticker: str
    price: float
    timestamp: datetime


class PriceCreate(PriceBase):
    pass


class PriceRead(PriceBase):
    model_config: ConfigDict = ConfigDict(from_attributes=True)
    id: int
