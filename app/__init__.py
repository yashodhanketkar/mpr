import os

from flask import Flask, render_template
from flask_assets import Environment

from .blueprints import auth, cross_performance, dashboard, home, performance, predictor, selector, reports
from .util.db import init_db
from .set_config import configure
from .util.assets import bundles


def handle_unauthorized(e):
    return render_template("errors/401.html"), 401


def handle_not_found(e):
    return render_template("errors/404.html"), 404


def handle_metod_not_allowed(e):
    return render_template("errors/405.html"), 405


def handle_range_not_satisfiable(e):
    return render_template("errors/416.html"), 416


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    if not os.path.isdir(app.instance_path):
        os.mkdir(app.instance_path)

    with app.app_context():
        configure()

    assets = Environment(app)
    assets.register(bundles)

    app.config.from_mapping(DATABASE=os.path.join(app.instance_path, "mpr.sqlite"))
    if not os.path.isfile(app.config["DATABASE"]):
        with app.app_context():
            init_db()

    for _bp in (auth, cross_performance, home, performance, predictor, selector, dashboard, reports):
        app.register_blueprint(_bp.bp)

    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(401, handle_unauthorized)
    app.register_error_handler(405, handle_metod_not_allowed)
    app.register_error_handler(416, handle_range_not_satisfiable)

    return app
