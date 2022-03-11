from .common import *
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hs6j037urx6iav+7#10%-vu4l4f5@@-1_zo)oft4g7$vf2$jmp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fcam',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'fcam',
        'PASSWORD': 'z{75w7E&/3]A_ff+'
    }
}