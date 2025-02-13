#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager, login_required
from flask_restful import Api

from common.exceptions.error_handling import enable_errorhandlers
from config import get_config
from database.connector import create_tables
from resources.booking_resource import BookingResource
from resources.bookings_resource import BookingsResource
from resources.customer_resource import CustomerResource
from resources.customers_resource import CustomersResource
from resources.events_resource import EventsResource
from resources.login_resource import LoginResource
from views.booking_view import BookingView
from views.calendar_view import CalendarView
from views.index_view import IndexView
from views.login_view import LoginView
from views.logout_view import LogoutView

create_tables()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.update(get_config("flask"))
enable_errorhandlers(app)

if app.config["BYPASS_LOGIN_REQUIRED"]:
    app.before_request(LoginResource().auto_login)

login_manager = LoginManager()
login_manager.init_app(app=app)
login_manager.user_loader(LoginResource().load_user)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "primary"

api = Api(app=app)

app.add_url_rule(rule="/", view_func=IndexView.as_view("index"))
app.add_url_rule(rule="/login", view_func=LoginView.as_view("login"))
app.add_url_rule(rule="/logout", view_func=LogoutView.as_view("logout"))
app.add_url_rule(rule="/booking", view_func=BookingView.as_view("booking"))
app.add_url_rule(
    rule="/calendar",
    view_func=login_required(
        CalendarView.as_view("calendar"),
    ),
)
api.add_resource(BookingResource, "/api/booking/<int:booking_id>")
api.add_resource(BookingsResource, "/api/booking")
api.add_resource(CustomerResource, "/api/customers/<int:customer_id>")
api.add_resource(CustomersResource, "/api/customers")
api.add_resource(EventsResource, "/api/events")


def main():
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
