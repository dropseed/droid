import os

from flask import Flask, request, Response, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from raven.contrib.flask import Sentry


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)  # for oauth http vs https behind proxy
app.secret_key = os.getenv("FLASK_SECRET_KEY", "development")
Sentry(app)  # uses SENTRY_DSN


@app.route("/incoming/slack/command/", methods=["POST"])
def slack_command():
    if not app.debug and not app.droid.slack_manager.request_is_valid(request):
        return Response(), 401

    handler = app.droid.slack_manager.command_request_handler
    if handler:
        return handler(app, request)

    return Response(), 501


@app.route("/incoming/slack/action/", methods=["POST"])
def slack_action():
    if not app.debug and not app.droid.slack_manager.request_is_valid(request):
        return Response(), 401

    handler = app.droid.slack_manager.action_request_handler
    if handler:
        return handler(app, request)

    return Response(), 501


@app.route("/incoming/slack/options/", methods=["POST"])
def slack_options():
    if not app.debug and not app.droid.slack_manager.request_is_valid(request):
        return Response(), 401

    handler = app.droid.slack_manager.options_request_handler
    if handler:
        return handler(app, request)

    return Response(), 501


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
