from datetime import timedelta as datetime_timedelta
SECRET_KEY = 'yandexlyceum_secret_key'
CSRF_ENABLED = True
PERMANENT_SESSION_LIFETIME = datetime_timedelta(minutes=15)
DEBUG = True
