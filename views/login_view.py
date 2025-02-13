from typing import Optional

from flask import render_template, request, redirect, url_for, flash
from flask.views import View
from flask_login import login_user, current_user
from werkzeug.datastructures import ImmutableMultiDict

from models.user import User
from services.user_service import UserService


class LoginView(View):
    methods = ["GET", "POST"]

    def __init__(self):
        self.user_service = UserService()

    def dispatch_request(self):
        if request.method == "POST":
            form: ImmutableMultiDict = request.form

            username = form.get("username")
            password = form.get("password")
            remember = bool(form.get("remember-me"))

            user: Optional[User] = self.user_service.retrieve_user_by_username(
                username=username
            )
            if user and self.user_service.validate_user(user, password):
                login_user(user, remember)
                return redirect(url_for("calendar"))
            else:
                flash("Wrong username or password!", category="warning")

        if current_user.is_authenticated:
            return redirect(url_for("calendar"))

        return render_template("login.html")
