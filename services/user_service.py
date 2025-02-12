from typing import Optional

from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from common.utils.transaction import transaction
from database.connector import get_session
from models.user import User


class UserService:

    @transaction
    def create_user(
        self,
        username: str,
        password: str,
        session: Session,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        email_address: Optional[str] = None,
    ) -> None:
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email_address=email_address,
            password=generate_password_hash(password),
        )
        session.add(user)

    @transaction
    def retrieve_user_by_id(
        self,
        user_id: int,
        session: Session,
    ) -> Optional[User]:
        return session.query(User).filter(User.id == user_id).first()

    def retrieve_user_by_username(
        self,
        username: str,
        session: Optional[Session] = None,
    ) -> Optional[User]:
        is_session_created_here: bool = False
        if session is None:
            session = get_session()
            is_session_created_here = True

        try:
            return (
                session.query(User)
                .filter(
                    User.username == username,
                )
                .first()
            )
        finally:
            if is_session_created_here:
                session.close()

    @transaction
    def is_user_exists(
        self,
        username: str,
        session: Session,
    ) -> bool:
        return bool(self.retrieve_user_by_username(username=username, session=session))

    def validate_user(
        self,
        user: User,
        password: str,
        session: Session,
    ) -> bool:
        if not user or not password:
            return False

        return check_password_hash(user.password, password=password)
