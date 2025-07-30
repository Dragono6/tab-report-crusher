from sqlalchemy.orm import Session
from . import models, schemas, auth
import uuid

# --- User CRUD ---

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(id=str(uuid.uuid4()), username=user.username, hashed_password=hashed_password, role="viewer")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Profile CRUD ---

def get_profile(db: Session, profile_id: str):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()

def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).offset(skip).limit(limit).all()

def update_profile(db: Session, profile_id: str, profile_data: schemas.ProfileCreate):
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if db_profile:
        db_profile.name = profile_data.name
        db_profile.json_data = profile_data.json_data
        db_profile.version = profile_data.version
        db.commit()
        db.refresh(db_profile)
    return db_profile

def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(**profile.dict(), id=str(uuid.uuid4()))
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# --- Rule CRUD ---

def get_rules_by_profile(db: Session, profile_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Rule).filter(models.Rule.profile_id == profile_id).offset(skip).limit(limit).all()

def create_rule_for_profile(db: Session, rule: schemas.RuleCreate, profile_id: str):
    db_rule = models.Rule(**rule.dict(), profile_id=profile_id, id=str(uuid.uuid4()))
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule 