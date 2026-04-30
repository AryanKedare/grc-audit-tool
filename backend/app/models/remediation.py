from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class RemediationTask(Base):
    __tablename__ = "remediation_tasks"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    control_id = Column(Integer, ForeignKey("controls.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default="medium")  # critical, high, medium, low
    status = Column(String, default="open")      # open, in_progress, resolved, risk_accepted
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    assignee = relationship("User", back_populates="remediation_tasks")
