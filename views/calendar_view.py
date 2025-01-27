from flask import render_template
from flask.views import View


class CalendarView(View):
    def dispatch_request(self):
        return render_template("calendar.html")
