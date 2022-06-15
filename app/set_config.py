"""set_config.py

Creates and provide the configuration to the main flask application.
"""
import os
import pathlib

from flask import current_app

APP_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.join(pathlib.Path(__file__).parent.parent.resolve())

MODELS_FOLDER = os.path.join(BASE_DIR, "model")
UPLOAD_FOLDER = os.path.join(APP_DIR, r"static\data")
TEST_FOLDER = os.path.join(APP_DIR, r"static\test")


def configure():
    """Provides configurateion to the application."""
    current_app.config.from_pyfile("config.py", silent=True)
    current_app.config["APP_DIR"] = APP_DIR
    current_app.config["BASBASE_DIR"] = BASE_DIR
    current_app.config["MODELS_FOLDER"] = MODELS_FOLDER
    current_app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    current_app.config["TEST_FOLDER"] = TEST_FOLDER
    for _FOLDER in (UPLOAD_FOLDER, TEST_FOLDER, MODELS_FOLDER):
        if not os.path.isdir(_FOLDER):
            os.mkdir(_FOLDER)
