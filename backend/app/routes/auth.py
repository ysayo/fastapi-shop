from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.auth_service import AuthService
from ..schemas.user import UserCreate, UserResponse, Token, VerifyRequest, ResendRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(email=user_data.email, password=user_data.password)

@router.post("/verify", response_model=Token)
def verify(data: VerifyRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    token = service.verify_code(email=data.email, code=data.code)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/resend-code", status_code=status.HTTP_202_ACCEPTED)
def resend_code(data: ResendRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    service.resend_code(email=data.email)
    return {"message": "Verification code sent"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = AuthService(db)
    token = service.authenticate(email=form_data.username, password=form_data.password)
    return {"access_token": token, "token_type": "bearer"}
