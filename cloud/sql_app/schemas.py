from pydantic import BaseModel
from typing import List, Optional

# --- Rule Schemas ---
class RuleBase(BaseModel):
    yaml_rule: str
    version: int

class RuleCreate(RuleBase):
    pass

class Rule(RuleBase):
    id: str
    profile_id: str

    class Config:
        orm_mode = True

# --- Profile Schemas ---
class ProfileBase(BaseModel):
    name: str
    json_data: str
    version: int

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: str
    rules: List[Rule] = []

    class Config:
        orm_mode = True

# --- User Schemas ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    role: str

    class Config:
        orm_mode = True

# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str 