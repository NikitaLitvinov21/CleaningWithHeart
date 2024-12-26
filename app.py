#! /usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import timedelta
from secrets import token_hex

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from database.connector import create_tables
from resources.booking_resource import BookingResource
from resources.login_resource import LoginResource
from views.index_view import IndexView
from views.login_view import LoginView
from views.booking_view import BookingView

load_dotenv()
create_tables()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["JWT_SECRET_KEY"] = token_hex(32)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)

api = Api(app=app)
jwt_manager = JWTManager(app=app)


app.add_url_rule(rule="/", view_func=IndexView.as_view(name="index"))
app.add_url_rule(rule="/login", view_func=LoginView.as_view(name="login"))
app.add_url_rule(rule="/booking", view_func=BookingView.as_view(name="booking"))
api.add_resource(BookingResource, "/api/booking")
api.add_resource(LoginResource, "/api/login")


def main():
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
