git push heroku main
heroku run python manage.py makemigrations
heroku run python manage.py migrate --run-syncdb