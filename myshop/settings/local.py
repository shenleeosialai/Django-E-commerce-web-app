from .base import *

DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shen',
        'USER': 'shen',
        'PASSWORD': 'shenlee',
        }
}
# ALLOWED_HOSTS = ['*']
