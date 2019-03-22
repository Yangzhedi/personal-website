from .base import * # NOQA
import pymysql

pymysql.install_as_MySQLdb()

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'site_db',
        'USER': 'root',
        'PASSWORD': 'PASSWORD',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }