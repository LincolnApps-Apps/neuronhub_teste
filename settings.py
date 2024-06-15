from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-+ms*uhuqu@q)v%qhp_k^yd6$_sxbjjf3(p2wrdv197#w3!_z4g'

DEBUG = True

ALLOWED_HOSTS = []

SHARED_APPS = [
    'django_tenants',  # Deve ser o primeiro
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'core_tenants',  # App onde estão os modelos Tenant e Domain
    'core_cadastros',  # App onde está o modelo Enterprise e CustomUser
    'core_website',  # App onde está a lógica de cadastro
    'core_vendas',    
]

TENANT_APPS = [
    'sis_inicial',
    'sis_cadastros',
    'sis_estoque',
    'sis_financeiro',
    'sis_logistica',
    'sis_fiscal',
    'sis_notificacoes',
]

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

DATABASE_ROUTERS = [
    'django_tenants.routers.TenantSyncRouter',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core_website.middleware.SessionTimeoutMiddleware',
    'core_website.middleware.CustomTenantMiddleware',
    'sis_inicial.middleware.NoCacheMiddleware',
]

ROOT_URLCONF = 'neuron_hub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'neuron_hub', 'sis_inicial', 'templates'),
            os.path.join(BASE_DIR, 'neuron_hub', 'core_website', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core_website.context_processors.tenant_schema',
            ],
        },
    },
]

WSGI_APPLICATION = 'neuron_hub.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'neuronhub1.2',
        'USER': 'neuronhub',
        'PASSWORD': 'Glock.40',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

TENANT_MODEL = "core_tenants.Tenant"
TENANT_DOMAIN_MODEL = "core_tenants.Domain"

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

AUTH_USER_MODEL = 'core_cadastros.CustomUser'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/protected/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = True

# # # # # # # # #  Configurações de segurança # # # # # # # # #
SESSION_COOKIE_SECURE = False  # Deve ser True em produção com HTTPS
# SECURE_SSL_REDIRECT = True  # Comentar para desenvolvimento sem HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_SECONDS = 31536000  # 1 ano (comentar para desenvolvimento sem HTTPS)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Comentar para desenvolvimento sem HTTPS
# SECURE_HSTS_PRELOAD = True  # Comentar para desenvolvimento sem HTTPS
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Comentar para desenvolvimento sem HTTPS
SECURE_REFERRER_POLICY = 'same-origin'
# CSRF_COOKIE_SECURE = True  # Comentar para desenvolvimento sem HTTPS
X_FRAME_OPTIONS = 'DENY'
