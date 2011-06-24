# -*- coding: utf-8 -*-
from django.db import models
from fetr_lib import live_stocks
from datetime import datetime
# Create your models here.

def is_bolsa_opened():
    opened = False
    now = datetime.now()
    if now.isoweekday() < 6: # Monday..Friday
        open_time = datetime(now.year, now.month, now.day, 8, 45)
        close_time = datetime(now.year, now.month, now.day, 17, 55)
        if now > open_time and now < close_time:
            opened = True
    return opened

def feed_stocks():
    for comp in Companies.objects.all():
        stock = live_stocks.parser_stocks(comp.feed_url)
    
        hour, minute = map(int, stock[2].split(":"))
        
        now = datetime.now()
        reg_time = datetime(now.year, now.month, now.day, hour, minute)
        Stoks(company = comp,
              last = stock[0],
              diff = stock[1],
              reg_time = reg_time,
              volume = stock[3]
              ).save()


def create_companies():
    Companies(name = "Telefónica", 
              tag = "TEF",
              feed_url = 'http://www.pcbolsa.com/movil/MovilCotizacion.aspx?ISIN=ES0178430E18&CodIndi=x&Plaza=55&Cotizacion=TELEFONICA'
              ).save()

class Companies(models.Model):
    name = models.CharField(max_length=100)
    tag =  models.CharField(max_length=5)
    feed_url = models.CharField(max_length=200)

class Stoks(models.Model):
    company = models.ForeignKey(Companies)
    last = models.FloatField()
    diff = models.FloatField()
    reg_time = models.DateTimeField()
    volume = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta(object):
        ordering = ['timestamp']
        
    def __unicode__(self):
        return u'%f %s %s' %(self.last, self.reg_time.isoformat(), self.timestamp.isoformat())

