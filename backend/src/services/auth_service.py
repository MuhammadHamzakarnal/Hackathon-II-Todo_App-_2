from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlmodel import Session, select

from src.models import User, UserCreate
from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        # Validate password length before hashing (bcrypt has 72-byte limit)
        if len(password.encode('utf-8')) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Validate password length before verification (bcrypt has 72-byte limit)
        if len(plain_password.encode('utf-8')) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user_id: int, email: str) -> str:
        expire = datetime.utcnow() + timedelta(days=settings.JWT_EXPIRY_DAYS)
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "exp": expire
        }
        return jwt.encode(
            to_encode,
            settings.BETTER_AUTH_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token,
                settings.BETTER_AUTH_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError:
            return None

    @staticmethod
    def register_user(session: Session, user_data: UserCreate) -> User:
        try:
            existing_user = session.exec(
                select(User).where(User.email == user_data.email)
            ).first()

            if existing_user:
                raise ValueError("Email already registered")

            user = User(
                email=user_data.email,
                password_hash=AuthService.hash_password(user_data.password)
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except ValueError:
            # Re-raise ValueError as-is
            raise
        except Exception as e:
            # Log the error for debugging
            print(f"Error registering user: {str(e)}")
            raise ValueError("Failed to register user due to a server error")

    @staticmethod
    def authenticate_user(
        session: Session, email: str, password: str
    ) -> Optional[User]:
        try:
            user = session.exec(
                select(User).where(User.email == email)
            ).first()

            if not user:
                return None

            if not AuthService.verify_password(password, user.password_hash):
                return None

            return user
        except Exception as e:
            # Log the error for debugging
            print(f"Error authenticating user: {str(e)}")
            return None

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        return session.get(User, user_id)
