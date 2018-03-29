import os

from mysite.settings import BASE_DIR

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# DATABASE - Postgres
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': '<DATABASE_NAME>',
#         'USER': '<USER>',
#         'PASSWORD': '<PASSWORD>',
#         'HOST': '<HOST_OR_IP>',
#         'PORT': '<PORT: 5432>',
#     }
# }

# DATABASE - SQLite3
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
