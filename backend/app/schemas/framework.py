from pydantic import BaseModel
from typing import List, Optional


class ControlSchema(BaseModel):
    id: int
    control_id: str
    title: str
    description: Optional[str]
    severity: str

    class Config:
        from_attributes = True


class DomainSchema(BaseModel):
    id: int
    name: str
    code: Optional[str]
    description: Optional[str]
    controls: List[ControlSchema] = []

    class Config:
        from_attributes = True


class FrameworkSchema(BaseModel):
    id: int
    name: str
    version: str
    slug: str
    description: Optional[str]
    domains: List[DomainSchema] = []

    class Config:
        from_attributes = True


class FrameworkListSchema(BaseModel):
    id: int
    name: str
    version: str
    slug: str
    description: Optional[str]

    class Config:
        from_attributes = True
