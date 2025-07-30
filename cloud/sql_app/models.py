from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    json_data = Column(Text)
    version = Column(Integer)

    rules = relationship("Rule", back_populates="profile")


class Rule(Base):
    __tablename__ = "rules"

    id = Column(String, primary_key=True, index=True)
    profile_id = Column(String, ForeignKey("profiles.id"))
    yaml_rule = Column(Text)
    version = Column(Integer)

    profile = relationship("Profile", back_populates="rules")

# TODO: Add models for Users, Runs, Deltas, etc. as needed. 