from sqlmodel import Session
from ..models import Log


class LogService:
    @staticmethod
    def create_log_entry(
        session: Session,
        user_id: int,
        action: str,
        details: str = None
    ):
        log_entry = Log(
            user_id=user_id,
            action=action,
            details=details
        )
        session.add(log_entry)
        session.commit()
