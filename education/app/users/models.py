from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    access = Column(Boolean, nullable=False, default=False)
    verified_email = Column(Boolean, nullable=False, default=False, insert_default=False)
    verification_code = Column(String, nullable=True)

