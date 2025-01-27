from flask import Flask, render_template


def enable_errorhandlers(app: Flask):

    @app.errorhandler(400)
    def bad_request(error):
        return render_template("exception.html", description="400 Bad Request!")

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("exception.html", description="404 Page not found!")

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template("exception.html", description="405 Method not allowed!")

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template(
            "exception.html",
            description="500 Internal Server Error!",
        )
