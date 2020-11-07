from os import environ
from .base import *
DEBUG = False
ADMINS = (
    (os.environ.get('ADMIN_NAME'), 
     os.environ.get('ADMIN_EMAIL')),
)
ALLOWED_HOSTS = ['buffteks.net', 'localhost', '127.0.0.1']
DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': os.environ.get('DB_NAME'),
       'USER': os.environ.get('DB_USER'),
       'PASSWORD': os.environ.get('DB_PASS'),        
    }
}
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')