# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pqVjew9NULFThypV1y9J15mboWUOAjGV24PJSeNB1Nszt34FzE'

# SECURITY WARNING: don't run with debug turned on in production!
if '/prod/' in BASE_DIR:
    DEBUG = False
    TEMPLATE_DEBUG = False
else:
    DEBUG = True
    TEMPLATE_DEBUG = True



# Application definition

INSTALLED_APPS = (
    'modeltranslation',
    'lactancia',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'debug_toolbar',
    'ratings',
    'meta',
) 



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.backends.ModelBackend',
    'lactancia.middleware.FilterPersistMiddleware',
    )

ROOT_URLCONF = 'django_project.urls'

WSGI_APPLICATION = 'django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django_db_geventpool.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'PVWCZsTKXv',
        'HOST': 'localhost',
        'PORT': '',
        'ATOMIC_REQUESTS': False,
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
           'MAX_CONNS': 20
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
ALLOWED_HOSTS = ['188.166.122.21', '0.0.0.0:9000', '127.0.0.1:9000','e-lactancia.org', 'www.e-lactancia.org',u'e-lactancia.org',u'www.e-lactancia.org']

LANGUAGE_CODE = 'es-ES'

#################
SITE_ID=1

#################
## Django-meta configuration
#################
META_SITE_PROTOCOL = 'http'
META_USE_SITES = True
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = False
META_SITE_NAME='e-lactancia.org'
META_SITE_TYPE='website'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

TIME_ZONE = 'Europe/Madrid'

USE_L10N = True

USE_TZ = True

# We decided to set a dir outside dev and prod developments to avoid
# overwriting
MEDIA_ROOT = '/home/django/media/'
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'


STATIC_ROOT = BASE_DIR + '/static/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    BASE_DIR + '/templates/',
    BASE_DIR + '/lactancia/templates/',
)



# GEOIP_PATH
GEOIP_PATH = '/home/django/geoip/'

# Necesario para que la sesion no cambie cuando el usuario pase de ser anonimo a estar
# registrado
SESSION_ENGINE = 'lactancia.session_backend'



# necesario para hacer funcionar el template
#  suit de administracion de django
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
	'django.core.context_processors.request',
)


# list of languages to translate:
gettext = lambda s: s
LANGUAGES= (
    ('en', _(u'Inglés')),
    ('es', _(u'Español')),
    
)

MODELTRANSLATION_LANGUAGES = ('en', 'es')

MODELTRANSLATION_DEFAULT_LANGUAGE = 'es'

MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'es'


# Django Suit configuration example
SUIT_CONFIG = {
    # header
     'ADMIN_NAME': 'Admin e-lactancia ',
     'HEADER_DATE_FORMAT': 'l, j F Y',
     'HEADER_TIME_FORMAT': 'H:i',

    # menu
     'SEARCH_URL': '/admin/lactancia/producto/',
     'MENU_OPEN_FIRST_CHILD': True,
     'MENU_EXCLUDE': ('auth','sites',),
     'MENU': (
         # Reorder app models
        {'label': _(u'Productos'), 'icon':'icon-heart', 'models': ('lactancia.producto', 'lactancia.alias', 'lactancia.otras_escrituras',)},
        {'label': _(u'Marcas'), 'icon':'icon-tags', 'models': ('lactancia.marca', )},
        {'label': _(u'Bibliografia'), 'icon':'icon-book', 'models': ('lactancia.bibliografia',)},
        {'label': _(u'Grupos y Riesgo'), 'icon':'icon-flag', 'models': ('lactancia.grupo','lactancia.riesgo',)},
        {'label': _(u'Comentarios y mensajes'), 'icon':'icon-bullhorn', 'models': ('lactancia.comentario','lactancia.mensaje',)},
        {'label': _(u'Landing'), 'icon':'icon-magnet', 'models': ('lactancia.cajita','lactancia.icono',)},
        {'label': _(u'Páginas estáticas'), 'icon':'icon-edit', 'models': ('lactancia.docs','lactancia.patrocinador','lactancia.aval',)},
        {'label': _(u'Países e idiomas'), 'icon':'icon-map-marker', 'models': ('lactancia.pais','lactancia.idioma',)},
     
     ), 

    
    # misc
     'LIST_PER_PAGE': 20
}


