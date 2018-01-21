from .base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ail0hx+l@10#g#8e--ps72fvjvn&m+9s&#8fgc=vo5%g275e^7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

