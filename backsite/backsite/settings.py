"""
Django settings for backsite project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3tyt)@rb#39wsp_png8z0^1eh+b+v&p(dsvj*@z@1$)uaub-c*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

<<<<<<< HEAD
ALLOWED_HOSTS = ["wte.wzz.moe", "127.0.0.1", "wte.wzz.ink"]
=======
ALLOWED_HOSTS = ["wte.wzz.moe", "127.0.0.1", "wte.wzz.ink", "cdn.wzz.ink"]
# STATIC_ROOT = "/home/wwwroot/wte.wzz.ink/static"
# STATIC_ROOT = "/home/wwwroot/wte.wzz.ink/static"
>>>>>>> Fei-dev


# Application definition

INSTALLED_APPS = [
    'compayu.apps.CompayuConfig',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'werkzeug_debugger_runserver',
    'django_extensions',
    'channels',
    'fei', #Fei-app
]
ASGI_APPLICATION = 'backsite.ws_router.application'
MIDDLEWARE = [
    # 'django.middleware.csrf.CsrfResponseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CHANNEL_LAYERS = {
    "default": {
        # 'BACKEND':'channels.layers.InMemoryChannelLayer'
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
# 
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    "http://127.0.0.1:5500",
    "https://www.wzz.ink",
    "https://cdn.wzz.ink",
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'backsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_backsite_default',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'db_compayu': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_backsite_compayu',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    },

    #  'db_Fei': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'compayu_dbl_fei',
    #     'USER': 'root',
    #     'PASSWORD': '1duolaSQL$',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3306',
    # },
}
DATABASE_APPS_MAPPING = {
    'compayu': 'db_compayu',
    'fei': 'db_compayu',
}

DATABASE_ROUTERS = ['backsite.db_router.DbRouter']

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.dirname(BASE_DIR) + '/static/'
print("STATIC_ROOT: "+STATIC_ROOT)


#飞哥专场
AUTH_USER_MODEL = 'fei.UserProfile' #使django自带user不起作用，用自己重写的

##七牛云
QINIU_ACCESS_KEY = '3j71vJK9qHMV9olqMfqdixed6_mOFBayKdlaieml' #AK
QINIU_SECRET_KEY = '2rHbG7oWJue_X7Zqw8eyAa6X7JNmQdGebviRnlER' #SK
QINIU_BUCKET_NAME = 'compayu-media'  #存储空间的名字
QINIU_BUCKET_DOMAIN = 'https://cdn.wzz.ink/'
QINIU_SECURE_URL = True      #使用https
DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuStorage' # 只用七牛托管动态生成的文件（例如用户上传的文件）

MEDIA_URL = QINIU_BUCKET_DOMAIN
MEDIA_ROOT = QINIU_BUCKET_DOMAIN