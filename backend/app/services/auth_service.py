from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..core.security import hash_password, verify_password, create_access_token
from ..models.user import User

class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, email: str, password: str) -> User:
        existing = self.repo.get_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        hashed = hash_password(password)
        return self.repo.create(email=email, hashed_password=hashed)

    def authenticate(self, email: str, password: str)-> str:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return create_access_token(data={"sub": user.email})
