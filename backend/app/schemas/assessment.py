from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AssessmentCreate(BaseModel):
    name: str
    framework_id: int


class ControlResponseCreate(BaseModel):
    status: str  # yes, partial, no, na
    evidence_notes: Optional[str] = None
    owner_name: Optional[str] = None


class ControlResponseSchema(BaseModel):
    id: int
    control_id: int
    status: str
    evidence_notes: Optional[str]
    owner_name: Optional[str]
    score: float

    class Config:
        from_attributes = True


class AssessmentSchema(BaseModel):
    id: int
    name: str
    framework_id: int
    status: str
    created_at: datetime
    responses: List[ControlResponseSchema] = []

    class Config:
        from_attributes = True


class ComplianceScore(BaseModel):
    framework: str
    overall_score: float
    total_controls: int
    answered: int
    domain_scores: List[dict]


class GapItem(BaseModel):
    control_id: str
    title: str
    severity: str
    domain: str
    status: str
    cross_framework_refs: List[str] = []
