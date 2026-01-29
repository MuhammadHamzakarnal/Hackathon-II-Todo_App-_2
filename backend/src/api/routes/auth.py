from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.database import get_session
from src.models import UserCreate, UserRead, UserLogin
from src.services import AuthService
from ..dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


class TokenResponse:
    def __init__(self, access_token: str, token_type: str, user: UserRead):
        self.access_token = access_token
        self.token_type = token_type
        self.user = user


@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreate,
    session: Annotated[Session, Depends(get_session)]
):
    try:
        user = AuthService.register_user(session, user_data)
        token = AuthService.create_access_token(user.id, user.email)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "created_at": user.created_at.isoformat()
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=dict)
async def login(
    credentials: UserLogin,
    session: Annotated[Session, Depends(get_session)]
):
    user = AuthService.authenticate_user(
        session, credentials.email, credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = AuthService.create_access_token(user.id, user.email)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }
    }


@router.get("/me", response_model=UserRead)
async def get_current_user(
    current_user: Annotated[UserRead, Depends(get_current_user)]
):
    return current_user
