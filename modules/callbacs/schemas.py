from pydantic import BaseModel
from typing import Optional


class Invoice(BaseModel):
    id: int
    title: Optional[str] = None
    customer: str
    total: float


class InvoiceEvent(BaseModel):
    description: str
    paid: bool


class InvoiceEventRecived(BaseModel):
    status: bool
