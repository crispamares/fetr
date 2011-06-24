# Create your views here.
from django.http import HttpResponse
from models import Stoks, Companies
import time, datetime

from django.core import serializers


def stocks(request, last=False):
    comp = request.GET.get('comp',None)
    timestring = request.GET.get('from',None) #timestring = "2005-09-01 12:30:09"
    time_format = "%Y-%m-%d %H:%M:%S"
    from_datetime = None
    if timestring:
        from_datetime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(timestring, time_format)))
        
    results = Stoks.objects.all()
    if comp:
        c = Companies.objects.get(tag=comp)
        results = results.filter(company=c)
    if from_datetime:
        results = results.filter(reg_time__gt=from_datetime)
    if last and results.exists():
        results = [results[0]]
        
    data = serializers.serialize("json", results, use_natural_keys=True)
    return HttpResponse(data)
