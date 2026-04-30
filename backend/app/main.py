from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import frameworks, assessments, remediation, auth
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GRC Audit Tool API",
    description="Multi-framework Governance, Risk & Compliance audit platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(frameworks.router, prefix="/api/frameworks", tags=["Frameworks"])
app.include_router(assessments.router, prefix="/api/assessments", tags=["Assessments"])
app.include_router(remediation.router, prefix="/api/remediation", tags=["Remediation"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "grc-audit-tool"}
