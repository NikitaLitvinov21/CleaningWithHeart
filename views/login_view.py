from flask import render_template
from flask.views import View


class LoginView(View):
    def dispatch_request(self):
        return render_template("login.html")
