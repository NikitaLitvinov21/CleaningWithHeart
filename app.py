#! /usr/bin/python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

from database.connector import create_tables
from resources.booking_resource import BookingResource
from views.index_view import IndexView
from views.login_view import LoginView

load_dotenv()
create_tables()

app = Flask(__name__, template_folder="templates", static_folder="static")
api = Api(app=app)


app.add_url_rule(rule="/", view_func=IndexView.as_view(name="index"))
app.add_url_rule(rule="/login", view_func=LoginView.as_view(name="login"))
api.add_resource(BookingResource, "/api/booking")


def main():
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
