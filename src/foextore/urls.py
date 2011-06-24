from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import django_cron
django_cron.autodiscover()

from stocks.views import stocks

urlpatterns = patterns('',
    # Example:
    # (r'^foextore/', include('foextore.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^stocks/$', stocks),
    (r'^stocks/last/$', stocks, {'last':True}),
)
