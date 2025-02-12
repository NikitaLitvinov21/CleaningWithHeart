from flask import render_template
from flask.views import View


class CustomersView(View):
    def dispatch_request(self):
        return render_template("customers.html")
