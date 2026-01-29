# =============================================================================
# BCRYPT VERSION COMPATIBILITY FIX - MUST BE FIRST!
# =============================================================================
# Problem: bcrypt 4.1.0+ removed the __about__ module that passlib uses for
# version detection, causing AttributeError on import.
# 
# Solution: Create a mock __about__ module BEFORE passlib tries to import it.
# This must happen at module load time, before any passlib imports.
# =============================================================================
import sys
import types

# Apply bcrypt fix BEFORE importing passlib
import bcrypt
if not hasattr(bcrypt, '__about__'):
    bcrypt_about = types.ModuleType('bcrypt.__about__')
    setattr(bcrypt_about, '__version__', getattr(bcrypt, '__version__', '4.0.0'))
    sys.modules['bcrypt.__about__'] = bcrypt_about
    bcrypt.__about__ = bcrypt_about

# NOW it's safe to import passlib
from passlib.context import CryptContext

from datetime import datetime, timedelta
from typing import Optional
import logging
import hashlib
import base64
from jose import jwt, JWTError
from sqlmodel import Session, select

from src.models import User, UserCreate
from src.config import settings

# Configure logging
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Authentication service with secure password handling.
    
    SECURITY NOTE ON 72-BYTE PASSWORD LIMIT:
    =========================================
    bcrypt has a hard limit of 72 bytes for passwords. This is a fundamental
    limitation of the Blowfish cipher used internally.
    
    INSECURE approaches (DO NOT USE):
    - Silent truncation: passwords "A"*72+"X" and "A"*72+"Y" become identical
    - Ignoring the limit: causes runtime errors on bcrypt 4.x
    
    SECURE approach (implemented here):
    - Pre-hash passwords with SHA-256 before bcrypt
    - SHA-256 produces 32 bytes (base64: 44 chars), always under 72 bytes
    - This preserves full password entropy while staying within bcrypt limits
    - Used by Dropbox, 1Password, and other security-focused applications
    """
    
    @staticmethod
    def _prepare_password(password: str) -> str:
        """
        Securely prepare password for bcrypt hashing.
        
        Uses SHA-256 pre-hashing to handle passwords of any length while
        preserving full entropy. The SHA-256 hash is base64-encoded to
        produce a 44-character string, well under bcrypt's 72-byte limit.
        
        This is the industry-standard approach used by:
        - Dropbox (documented in their security blog)
        - 1Password
        - Many other security-conscious applications
        
        Args:
            password: The raw password string
            
        Returns:
            A base64-encoded SHA-256 hash of the password
        """
        # SHA-256 hash the password to handle any length securely
        password_bytes = password.encode('utf-8')
        sha256_hash = hashlib.sha256(password_bytes).digest()
        # Base64 encode to get a string (44 chars, well under 72 bytes)
        return base64.b64encode(sha256_hash).decode('ascii')

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256 pre-hashing + bcrypt."""
        prepared = AuthService._prepare_password(password)
        return pwd_context.hash(prepared)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        prepared = AuthService._prepare_password(plain_password)
        return pwd_context.verify(prepared, hashed_password)

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
        logger.info(f"[register_user] Attempting to register user: {user_data.email}")
        
        existing_user = session.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing_user:
            logger.warning(f"[register_user] Email already registered: {user_data.email}")
            raise ValueError("Email already registered")

        try:
            logger.info("[register_user] Hashing password...")
            password_hash = AuthService.hash_password(user_data.password)
            logger.info("[register_user] Password hashed successfully")
        except Exception as e:
            logger.error(f"[register_user] Password hashing failed: {type(e).__name__}: {e}")
            raise ValueError(f"Password hashing failed: {str(e)}")

        try:
            user = User(
                email=user_data.email,
                password_hash=password_hash
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            logger.info(f"[register_user] User registered successfully: {user.id}")
            return user
        except Exception as e:
            logger.error(f"[register_user] Database error: {type(e).__name__}: {e}")
            raise ValueError(f"Database error: {str(e)}")

    @staticmethod
    def authenticate_user(
        session: Session, email: str, password: str
    ) -> Optional[User]:
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user:
            return None

        if not AuthService.verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        return session.get(User, user_id)
