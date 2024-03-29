"""assets.py

Works as
    1. Compliler for the scss files.
    2. Bundler for js and resulted css files.
"""


from flask_assets import Bundle

bundles = {
    "home_js": Bundle(
        "scripts/vendor/bootstrap.bundle.js",
        "scripts/mpr.js",
        filters="jsmin",
        output="gen/home.%(version)s.js",
    ),
    "home_css": Bundle(
        "css/vendor/bootstrap.css",
        "css/base.scss",
        depends=["css/*.scss"],
        filters="libsass",
        output="gen/home.%(version)s.css",
    ),
}
