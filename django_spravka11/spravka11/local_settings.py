DATABASES = {
    'default': {
    'ENGINE': 'mysql.connector.django',
    'NAME': 'django',
    'USER': 'root',
    'PASSWORD': 'root',
    'HOST': 'localhost',
    'PORT': '3306',
}
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr'
    },
}