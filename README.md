# Weightage based training, testing, selection and prediction system

----

This is an automated supervised learning system. This system allows users without coding experience to create the best suited model for the prediction task. This system stores the best models for future use. All the other models are also stored for further uses.

This system employs skit-learns supervised learning models as templates. The application uses web UI with the help of flask module.

## Table of contents

[DEPENDENCIES](DEPENDENCIES)\
[INSTALLATION](INSTALLATION)\
[LICENSE](LICENSE)

## DEPENDENCIES

- [Python 3](https://www.python.org/downloads/)
- [Scikit-learn](https://pypi.org/project/scikit-learn/) - This module is used for model creation and performance analysis.
- [Pandas](https://pypi.org/project/pandas/) - This module is used to handle data structures.
- [Pygal](https://pypi.org/project/pygal/) - This module is used for generating dynamic charts.
- [Flask](https://pypi.org/project/Flask/) - This module is used for webUI.

## INSTALLATION

Open bash or terminal and enter following commands

```sh
# go to project directory
cd /path_to_folder/
```
Inside main directory enter following commands

```sh
# create and activate virtual environment
python -m venv venv
venv\Scripts\activate.bat

# install dependencies in virtual environment
pip install -r requirements.txt
```
This will install all dependencies in virtual environment

## Configuration

1. Create new folder **instance**

2. Create new file **config.py** inside instance folder.

3. Run following command to generate $secret_token

    ```sh
    # generate secret token for flask application
    python -c "import secrets;print(secrets.token_hex(32))"
    ```

4. Add $secret_token generated to the config file

    ```python
    SECRETE_KEY=$secret_token
    ```

## Execute

Enter following command

```sh
flask run
```

This will give you following message

```sh
 * Serving Flask app 'run' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: ***-***-***
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

- Use the path provided that is http://127.0.0.1:5000/ inside your preferred web browser

---
&copy; 2022 - Yashodhan Ketkar
