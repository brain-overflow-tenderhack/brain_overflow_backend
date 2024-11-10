from pydantic import BaseModel
from typing import List


class SessionData(BaseModel):
    title: str = None
    is_guarantee_needed: bool = False
    is_license_needed: bool = False
    license_files: List[str] = None
    delivery_schedule: bool = False
    delivery_stage: bool = False
    price: int = None
    technical_specification: List[dict] = None


class Parameters(BaseModel):
    title: bool = False
    is_guarantee_needed: bool = False
    is_license_needed: bool = False
    license_files: bool = False
    delivery_schedule: bool = False
    delivery_stage: bool = False
    price: bool = False
    technical_specification: bool = False
