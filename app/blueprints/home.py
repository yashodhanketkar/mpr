"""home.py blueprint

Provides the home page and landing page to the web application.
"""
from flask import Blueprint, render_template

bp = Blueprint("home", __name__)


@bp.route("/")
def home():
    """Provieds the home page to the application

    Returns:
        home.html (html_template): Home page of the applcaiton
    """
    return render_template("main/home.html")
