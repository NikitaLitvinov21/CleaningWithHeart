from flask import render_template
from flask.views import View


class BookingView(View):
    def dispatch_request(self):
        return render_template("booking.html")
