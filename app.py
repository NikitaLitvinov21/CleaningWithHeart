#! /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager, login_required
from flask_restful import Api

from common.exceptions.error_handling import enable_errorhandlers
from config import get_config
from database.connector import create_tables
from resources.addresses_resource import AddressesResource
from resources.booking_resource import BookingResource
from resources.bookings_resource import BookingsResource
from resources.customer_resource import CustomerResource
from resources.customers_resource import CustomersResource
from resources.events_resource import EventsResource
from resources.login_resource import LoginResource
from views.booking_view import BookingView
from views.calendar_view import CalendarView
from views.customers_view import CustomersView
from views.index_view import IndexView
from views.login_view import LoginView
from views.logout_view import LogoutView
from workers.twilio_worker import TwilioWorker

create_tables()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.update(get_config("flask"))
enable_errorhandlers(app)

if app.config["BYPASS_LOGIN_REQUIRED"]:
    print("SECURITY WARNING: BYPASS_LOGIN_REQUIRED Enabled!")
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
app.add_url_rule(
    rule="/customers",
    view_func=login_required(
        CustomersView.as_view("customers"),
    ),
)

api.add_resource(BookingResource, "/api/booking/<int:booking_id>")
api.add_resource(BookingsResource, "/api/booking")
api.add_resource(CustomerResource, "/api/customers/<int:customer_id>")
api.add_resource(CustomersResource, "/api/customers")
api.add_resource(EventsResource, "/api/events")
api.add_resource(AddressesResource, "/api/addresses")

twilio_worker = TwilioWorker(get_config("twilio"))
twilio_worker.run()


def main():
    app.run(**get_config("server"))


if __name__ == "__main__":
    main()
