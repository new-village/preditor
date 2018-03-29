# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<DATABASE_NAME>',
        'USER': '<USER>',
        'PASSWORD': '<PASSWORD>',
        'HOST': '<HOST_OR_IP>',
        'PORT': '<PORT: 5432>',
    }
}