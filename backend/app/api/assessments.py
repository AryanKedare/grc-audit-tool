from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.assessment import Assessment, ControlResponse
from app.models.framework import Framework, Control, Domain
from app.models.user import User
from app.schemas.assessment import (
    AssessmentCreate, AssessmentSchema, ControlResponseCreate,
    ComplianceScore, GapItem
)
from app.services.auth_service import get_current_user

router = APIRouter()

STATUS_SCORES = {"yes": 1.0, "partial": 0.5, "no": 0.0, "na": None}


@router.post("/", response_model=AssessmentSchema, status_code=201)
def create_assessment(
    data: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    fw = db.query(Framework).filter(Framework.id == data.framework_id).first()
    if not fw:
        raise HTTPException(status_code=404, detail="Framework not found")
    assessment = Assessment(name=data.name, framework_id=data.framework_id, owner_id=current_user.id)
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment


@router.get("/", response_model=List[AssessmentSchema])
def list_assessments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Assessment).filter(Assessment.owner_id == current_user.id).all()


@router.get("/{assessment_id}", response_model=AssessmentSchema)
def get_assessment(assessment_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    a = db.query(Assessment).filter(
        Assessment.id == assessment_id, Assessment.owner_id == current_user.id
    ).first()
    if not a:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return a


@router.put("/{assessment_id}/controls/{control_id}")
def respond_to_control(
    assessment_id: int,
    control_id: int,
    data: ControlResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id, Assessment.owner_id == current_user.id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    score_val = STATUS_SCORES.get(data.status, 0.0)
    response = db.query(ControlResponse).filter(
        ControlResponse.assessment_id == assessment_id,
        ControlResponse.control_id == control_id,
    ).first()

    if response:
        response.status = data.status
        response.evidence_notes = data.evidence_notes
        response.owner_name = data.owner_name
        response.score = score_val if score_val is not None else response.score
    else:
        response = ControlResponse(
            assessment_id=assessment_id,
            control_id=control_id,
            status=data.status,
            evidence_notes=data.evidence_notes,
            owner_name=data.owner_name,
            score=score_val or 0.0,
        )
        db.add(response)
    db.commit()
    return {"message": "Control response saved"}


@router.get("/{assessment_id}/score", response_model=ComplianceScore)
def get_compliance_score(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id, Assessment.owner_id == current_user.id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    fw = db.query(Framework).filter(Framework.id == assessment.framework_id).first()
    responses = {r.control_id: r for r in assessment.responses}
    domain_scores = []
    total_score = 0.0
    total_applicable = 0

    for domain in fw.domains:
        d_score = 0.0
        d_applicable = 0
        for control in domain.controls:
            resp = responses.get(control.id)
            if resp and resp.status != "na":
                d_score += resp.score
                d_applicable += 1
                total_applicable += 1
                total_score += resp.score
        domain_scores.append({
            "domain": domain.name,
            "score": round((d_score / d_applicable * 100) if d_applicable > 0 else 0, 1),
            "controls_assessed": d_applicable,
        })

    all_controls = sum(len(d.controls) for d in fw.domains)
    return ComplianceScore(
        framework=fw.name,
        overall_score=round((total_score / total_applicable * 100) if total_applicable > 0 else 0, 1),
        total_controls=all_controls,
        answered=len(responses),
        domain_scores=domain_scores,
    )


@router.get("/{assessment_id}/gaps", response_model=List[GapItem])
def get_gaps(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id, Assessment.owner_id == current_user.id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    fw = db.query(Framework).filter(Framework.id == assessment.framework_id).first()
    responses = {r.control_id: r for r in assessment.responses}
    gaps = []

    for domain in fw.domains:
        for control in domain.controls:
            resp = responses.get(control.id)
            if not resp or resp.status in ("no", "partial"):
                cross_refs = [m.control_id for m in control.mapped_controls]
                gaps.append(GapItem(
                    control_id=control.control_id,
                    title=control.title,
                    severity=control.severity,
                    domain=domain.name,
                    status=resp.status if resp else "unanswered",
                    cross_framework_refs=cross_refs,
                ))
    gaps.sort(key=lambda g: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(g.severity, 4))
    return gaps
