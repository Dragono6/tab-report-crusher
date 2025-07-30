from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, timedelta
import socketio

from .sql_app import auth, crud, models, schemas
from .sql_app.database import SessionLocal, engine
from .sql_app.auth import get_current_user_from_token


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TAB Report Crusher - Cloud Sync API",
    description="Syncs profiles, rules, and other settings.",
    version="0.1.0"
)

# --- Database Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- User Model & Schema (for auth) ---
# TODO: Move these to models.py and schemas.py respectively
class User(models.Base):
    __tablename__ = "users"
    id = models.Column(models.Integer, primary_key=True, index=True)
    username = models.Column(models.String, unique=True, index=True)
    hashed_password = models.Column(models.String)
    role = models.Column(models.String, default="viewer") # 'viewer' or 'manager'

class UserCreate(schemas.BaseModel):
    username: str
    password: str

class UserInDB(schemas.BaseModel):
    username: str
    role: str

# --- Authentication Endpoints ---
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


# --- Dependency for verifying Manager role ---
async def get_current_manager(current_user: dict = Depends(get_current_user_from_token)):
    if current_user.get("role") != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have manager privileges"
        )
    return current_user

# --- WebSocket Server ---
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(sio, app)

@sio.event
async def connect(sid, environ):
    print(f"WebSocket connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"WebSocket disconnected: {sid}")

# TODO: Add events for broadcasting profile/rule updates

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the TAB Report Crusher Cloud Sync API"}

# --- Profiles Endpoints ---

@app.post("/profiles/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    # TODO: Add check for existing profile by name
    return crud.create_profile(db=db, profile=profile)

@app.get("/profiles/", response_model=list[schemas.Profile])
def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profiles = crud.get_profiles(db, skip=skip, limit=limit)
    return profiles

@app.get("/profiles/{profile_id}", response_model=schemas.Profile)
def read_profile(profile_id: str, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

# Example of a protected endpoint
@app.put("/profiles/{profile_id}", response_model=schemas.Profile)
async def update_profile(
    profile_id: str,
    profile: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_manager)
):
    db_profile = crud.update_profile(db, profile_id, profile)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Broadcast this update to all connected clients
    await sio.emit('profile_updated', {'profile_id': profile_id, 'name': profile.name})
    
    return db_profile

# --- Rules Endpoints ---

@app.post("/profiles/{profile_id}/rules/", response_model=schemas.Rule)
def create_rule_for_profile(
    profile_id: str, rule: schemas.RuleCreate, db: Session = Depends(get_db)
):
    # TODO: Ensure profile exists before adding rule
    return crud.create_rule_for_profile(db=db, rule=rule, profile_id=profile_id)

@app.get("/rules/", response_model=list[schemas.Rule])
def read_rules(profile_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rules = crud.get_rules_by_profile(db, profile_id=profile_id, skip=skip, limit=limit)
    return rules

# TODO: Implement /auth endpoint
# TODO: Implement /deltas endpoint
# TODO: Implement /versions endpoint

# Placeholder for a protected route
@app.get("/manager/test", dependencies=[Depends(get_current_manager)])
def test_manager_only_route():
    # This route is now protected by the get_current_manager dependency.
    return {"message": "This route is for Managers only."} 