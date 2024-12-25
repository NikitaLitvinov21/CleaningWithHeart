from typing import Optional

from flask import Response, jsonify, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from models.user import User
from services.user_service import UserService


class LoginResource(Resource):

    def __init__(self):
        self.user_service = UserService()

    def post(self) -> Response:
        data = request.json
        username: str = data.get("username")
        password: str = data.get("password")

        if not username and not password:
            return Response(
                status=400,
                content_type="application/json",
                response='{"message": "Username and Password are required!"}',
            )

        user: Optional[User] = self.user_service.retrieve_user_by_username(
            username=username,
        )

        if user and self.user_service.validate_user(
            user=user,
            password=password,
        ):
            access_token = create_access_token(identity=user.id)
            return jsonify(
                {
                    "username": user.username,
                    "access_token": access_token,
                }
            )
        else:
            return Response(
                status=401,
                content_type="application/json",
                response='{"message": "Invalid credentials"}',
            )
