export FLASK_APP="flaskr:create_app('development.py')";
export FLASK_ENV=development;
export VENV_SOURCE=env;
source "$VENV_SOURCE/bin/activate";
flask db init;
flask db migrate;
flask db upgrade;