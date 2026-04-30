from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Cross-framework control mapping (many-to-many)
control_crosswalk = Table(
    "control_crosswalk",
    Base.metadata,
    Column("control_id", Integer, ForeignKey("controls.id"), primary_key=True),
    Column("mapped_control_id", Integer, ForeignKey("controls.id"), primary_key=True),
)


class Framework(Base):
    __tablename__ = "frameworks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)       # e.g. "NIST CSF"
    version = Column(String, nullable=False)    # e.g. "2.0"
    slug = Column(String, unique=True)          # e.g. "nist-csf-2"
    description = Column(Text)
    domains = relationship("Domain", back_populates="framework")


class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True)
    framework_id = Column(Integer, ForeignKey("frameworks.id"))
    name = Column(String, nullable=False)       # e.g. "Protect"
    code = Column(String)                       # e.g. "PR"
    description = Column(Text)
    framework = relationship("Framework", back_populates="domains")
    controls = relationship("Control", back_populates="domain")


class Control(Base):
    __tablename__ = "controls"

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id"))
    control_id = Column(String, nullable=False) # e.g. "PR.AA-01"
    title = Column(String, nullable=False)
    description = Column(Text)
    severity = Column(String, default="medium") # critical, high, medium, low
    domain = relationship("Domain", back_populates="controls")
    mapped_controls = relationship(
        "Control",
        secondary=control_crosswalk,
        primaryjoin=id == control_crosswalk.c.control_id,
        secondaryjoin=id == control_crosswalk.c.mapped_control_id,
    )
