from flask import redirect, url_for, flash
from flask_login import logout_user
from flask.views import View


class LogoutView(View):
    def dispatch_request(self):
        logout_user()
        flash("You successfully logout!", category="success")
        return redirect(url_for("login"))
