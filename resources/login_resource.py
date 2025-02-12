from typing import Optional

from flask_login import login_user
from flask_restful import Resource

from models.user import User
from services.user_service import UserService


class LoginResource(Resource):

    def __init__(self):
        self.user_service = UserService()

    def load_user(self, user_id) -> Optional[User]:
        return self.user_service.retrieve_user_by_id(user_id=user_id)

    def auto_login(self):
        user_service = UserService()
        user: Optional[User] = user_service.retrieve_user_by_id(user_id=1)
        if user:
            login_user(user)
