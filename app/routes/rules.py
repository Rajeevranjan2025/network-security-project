from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.schemas.rule import RuleCreate, RuleResponse
from app.models.rule import Rule
from app.services.security_engine import create_security_log

router = APIRouter(prefix="/rules", tags=["Rules"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RuleResponse)
def add_rule(rule: RuleCreate, db: Session = Depends(get_db)):
    new_rule = Rule(
        device_id=rule.device_id,
        rule_type=rule.rule_type,
        target=rule.target,
        description=rule.description
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)

    create_security_log(
        db=db,
        device_id=rule.device_id,
        message=f"Rule added: {rule.rule_type.upper()} {rule.target}",
        severity="info"
    )

    return new_rule

@router.get("/")
def list_rules(db: Session = Depends(get_db)):
    return db.query(Rule).all()

@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()

    if not rule:
        return {"error": "Rule not found"}

    create_security_log(
        db=db,
        device_id=rule.device_id,
        message=f"Rule deleted: {rule.description}",
        severity="warning"
    )

    db.delete(rule)
    db.commit()

    return {"message": "Rule deleted and logged"}
