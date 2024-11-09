from pydantic import BaseModel


class QuoteCard(BaseModel):
    url: str
    title: str
    contract_security: str
    licenses: str
    delivery_schedule: str
    delivery_stage: str
    price: int
    technical_specification: str


class Parameters(BaseModel):
    title: bool = False
    contract_security: bool = False
    licenses: bool = False
    delivery_schedule: bool = False
    delivery_stage: bool = False
    price: bool = False
    technical_specification: bool = False
