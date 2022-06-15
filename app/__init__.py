import os

from flask import Flask


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    if not os.path.isdir(app.instance_path):
        os.mkdir(app.instance_path)

    from .set_config import configure

    with app.app_context():
        configure()

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

    return app
