import os

from flask import Flask, render_template


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    if not os.path.isdir(app.instance_path):
        os.mkdir(app.instance_path)

    from .set_config import configure

    with app.app_context():
        configure()

    from .util.assets import bundles
    from flask_assets import Environment

    assets = Environment(app)
    assets.register(bundles)

    app.config.from_mapping(DATABASE=os.path.join(app.instance_path, "mpr.sqlite"))
    if not os.path.isfile(app.config["DATABASE"]):
        from .db import init_db

        with app.app_context():
            init_db()

    from .blueprints import (
        auth,
        cross_performance,
        dashboard,
        home,
        performance,
        predictor,
        selector,
    )

    for _bp in (
        auth,
        cross_performance,
        home,
        performance,
        predictor,
        selector,
        dashboard,
    ):
        app.register_blueprint(_bp.bp)
    
    from werkzeug.exceptions import BadRequest

    def handle_not_found(BadRequest):
        return render_template("errors/404.html")

    def handle_unauthorized(BadRequest):
        return render_template("errors/401.html")

    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(401, handle_unauthorized)

    return app
