from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    framework_id = Column(Integer, ForeignKey("frameworks.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="in_progress")  # in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="assessments")
    responses = relationship("ControlResponse", back_populates="assessment")


class ControlResponse(Base):
    __tablename__ = "control_responses"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    control_id = Column(Integer, ForeignKey("controls.id"))
    status = Column(String)   # yes, partial, no, na
    evidence_notes = Column(Text, nullable=True)
    owner_name = Column(String, nullable=True)
    score = Column(Float, default=0.0)  # 0=no, 0.5=partial, 1=yes
    updated_at = Column(DateTime, default=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="responses")
