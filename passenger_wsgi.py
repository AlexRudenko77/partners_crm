# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u2313522/data/www/bonus-internet.ru/internetnik/')
sys.path.insert(1, '/var/www/u2313522/data/djangoenv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'internetnik.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()