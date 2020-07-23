export VENV_SOURCE=env;
source "$VENV_SOURCE/bin/activate";
python manage.py db init;
python manage.py db migrate;
python manage.py db upgrade;
python filldb.py;