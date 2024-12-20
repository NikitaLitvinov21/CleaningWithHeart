from datetime import date
from typing import Optional

from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from database.connector import get_session
from models.user import User


class UserService:

    def create_user(
        self,
        username: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        email_address: Optional[str] = None,
        birth_date: Optional[date] = None,
        session: Session = get_session(),
    ) -> None:
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email_address=email_address,
            birth_date=birth_date,
            password=generate_password_hash(password),
        )
        session.add(user)
        session.commit()

    def retrieve_user_by_username(
        self,
        username: str,
        session: Session = get_session(),
    ) -> Optional[User]:
        return session.query(User).filter(User.username == username).first()

    def is_user_exists(
        self,
        username: str,
        session: Session = get_session(),
    ) -> bool:
        return bool(self.retrieve_user_by_username(username=username, session=session))

    def validate_user(
        self,
        user: User,
        password: str,
        session: Session = get_session(),
    ) -> bool:
        if not user or not password:
            return False

        return check_password_hash(user.password, password=password)
