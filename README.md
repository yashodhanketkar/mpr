MPR
===

Weightage based training, testing, selection and prediction system

Table of contents
-----------------

-	[Introduction](#introduction)
	-	[Dependencies](#dependencies)
-	[Installation and Usage](#installation-and-usage)
	-	[Setup](#setup)
	-	[Configuration](#configuration)
	-	[Run](#run)
-	[LICENSE](#license)

Introduction
------------

This is an automated supervised learning system. This system allows users without coding experience to create the best suited model for the prediction task. This system stores the best models for future use. All the other models are also stored for further uses.

This system employs skit-learns supervised learning models as templates. The application uses web UI with the help of flask module.

### Dependencies

-	[Python 3](https://www.python.org/downloads/)
-	[Scikit-learn](https://pypi.org/project/scikit-learn/)[^1]
-	[Pandas](https://pypi.org/project/pandas/)[^2]
-	[Pygal](https://pypi.org/project/pygal/)[^3]
-	[Flask](https://pypi.org/project/Flask/)[^4]

[^1]: Model creation and performance analysis.

[^2]: Handling data structures.

[^3]: Generation of dynamic charts.

[^4]: Support and rendering of WebUI.

Installation and Usage
----------------------

### Setup

Setup the project

1.	Clone this repository into your local machine.
2.	Move to the project directory. Using `cd mpr`.
3.	Setup virtual environment using `uv venv`.
4.	Install dependencies using `uv sync`.

### Configuration

Configuration of environment variables

```sh
# with make
-----------
make setup

# without make
--------------
# Create new directory `instance` and create new file `instance/config.py`.
mkdir instance
touch instance/config.py

# Generate secret token for flask application
echo "SECRET_KEY = '$(openssl rand -base64 32)'" > ./instance/config.py

# you can also use following command instead of openssl
python -c "import secrets;print(secrets.token_hex(32))" # modern systems
# or
python3 -c "import secrets;print(secrets.token_hex(32))" # legacy systems
```

### Run

Run the project in `development | production` mode

```sh
# with make
-----------
# Run the project in development mode
make dev

# Run the project in production mode
make run

# without make
--------------
# Run the project in development mode
uv run flask run

# Run the project in production mode
uv run main
```

LICENSE
-------

This project is licensed under the terms of the [MIT license](./LICENSE). See the [license](./LICENSE) file for details.

Copyright (c) 2022-2026 Yashodhan Ketkar
