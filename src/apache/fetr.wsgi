import os
import sys


path = ['/home/jmorales/proyectos/fetr/src/', 
        '/home/jmorales/proyectos/fetr/src/foextore',
        '/home/jmorales/proyectos/fetr/src/foextore/news_paper',
        '/home/jmorales/proyectos/fetr/src/foextore/stocks',
        '/home/jmorales/proyectos/fetr/src/foextore/django_cron']

sys.path += path

os.environ['DJANGO_SETTINGS_MODULE'] = 'foextore.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
