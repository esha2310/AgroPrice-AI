from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured
BASE_DIR=Path(__file__).resolve().parent.parent
DEBUG=os.environ.get('DEBUG','1')=='1'
SECRET_KEY=os.environ.get('SECRET_KEY','local-development-only-agroprice-do-not-use-publicly')
if not DEBUG and (SECRET_KEY.startswith(('local-development','GENERATE_')) or len(SECRET_KEY)<40):raise ImproperlyConfigured('Set a unique SECRET_KEY of at least 40 characters before production.')
ALLOWED_HOSTS=[s.strip() for s in os.environ.get('ALLOWED_HOSTS','localhost,127.0.0.1,[::1]').split(',') if s.strip()]
CSRF_TRUSTED_ORIGINS=[s.strip() for s in os.environ.get('CSRF_TRUSTED_ORIGINS','').split(',') if s.strip()]
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','accounts']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='config.wsgi.application'
DATA_DIR=Path(os.environ.get('DATA_DIR',str(BASE_DIR)));DATA_DIR.mkdir(parents=True,exist_ok=True)
DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':DATA_DIR/'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS=[{'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},{'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},{'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE='en-us';TIME_ZONE='Asia/Dhaka';USE_I18N=True;USE_TZ=True
STATIC_URL='static/';STATIC_ROOT=BASE_DIR/'staticfiles';DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
SESSION_COOKIE_HTTPONLY=True;SESSION_COOKIE_SAMESITE='Lax';SESSION_COOKIE_AGE=60*60*24*7
SESSION_COOKIE_SECURE=not DEBUG;CSRF_COOKIE_SECURE=not DEBUG;SECURE_SSL_REDIRECT=not DEBUG
SECURE_HSTS_SECONDS=31536000 if not DEBUG else 0;SECURE_HSTS_INCLUDE_SUBDOMAINS=not DEBUG;SECURE_HSTS_PRELOAD=not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF=True;X_FRAME_OPTIONS='DENY';SECURE_REFERRER_POLICY='same-origin'
# Set only behind a reverse proxy you control that strips untrusted forwarded headers.
if os.environ.get('TRUST_PROXY','0')=='1':SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO','https')
DATA_UPLOAD_MAX_MEMORY_SIZE=32768
CACHES={'default':{'BACKEND':'django.core.cache.backends.locmem.LocMemCache'}}
