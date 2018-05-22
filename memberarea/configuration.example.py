from datetime import timedelta
#########################
#   Required settings   #
#########################

# This is a list of valid fully-qualified domain names (FQDNs) for the Memberarea server. Memberarea will not permit
# access to the server via any other hostnames. The first FQDN in the list will be treated as the preferred name.
#
# Example: ALLOWED_HOSTS = ['memberarea.example.com', 'memberarea.internal.local']
ALLOWED_HOSTS = []

# Database configuration.
DATABASE = {
    'ENGINE': 'django.db.backends.mysql',   # Database engine
    'NAME': 'memberarea',     # Database name
    'USER': '',               # Database username
    'PASSWORD': '',           # Database password
    'HOST': 'localhost',      # Database server
    'PORT': '',               # Database port (leave blank for default)
    'OPTIONS': {
        'sql_mode': 'STRICT_ALL_TABLES',
    },
}

# This key is used for secure generation of random numbers and strings. It must never be exposed outside of this file.
# For optimal security, SECRET_KEY should be at least 50 characters in length and contain a mix of letters, numbers, and
# symbols. Memberarea will not run without this defined. For more information, see
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = 'replace-this-with-actual-secret'

# API Token Timeouts
TOKEN_TIMEOUT = timedelta(minutes=20)
TOKEN_REFRESH_TIMEOUT = timedelta(hours=2)

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': TOKEN_TIMEOUT,
    'REFRESH_TOKEN_LIFETIME': TOKEN_REFRESH_TIMEOUT,
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': "replace-this-with-actual-secret",
    'AUTH_HEADER_TYPES': ('JWT', ),
}


#########################
#   Optional settings   #
#########################

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Time zone (default: UTC)
TIME_ZONE = 'UTC'
