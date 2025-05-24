python manage.py makemigrations authentication
python manage.py makemigrations education
python manage.py makemigrations payment
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn -b 0.0.0.0 -p 8000 config.wsgi:application
