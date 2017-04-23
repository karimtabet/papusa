import os

import dj_database_url

from .base import *

DEBUG = True

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

if AWS_STORAGE_BUCKET_NAME and AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


DATABASES = {
    'default': dj_database_url.config(
        default=os.environ['DB_URL'])
}


WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'INDEX': 'papusa'
    }
}


CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'KEY_PREFIX': 'papusa',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    }
}

# Use the cached template loader
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)


try:
    from .local import *
except ImportError:
    pass
