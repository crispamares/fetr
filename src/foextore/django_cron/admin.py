'''
Created on 24/06/2011

@author: crispamares
'''
from models import Cron, Job
from django.contrib import admin

admin.site.register(Cron)
admin.site.register(Job)

