# Create your views here.
from django.http import HttpResponse
from models import NewsPapers, KeyWords
import time, datetime

from django.core import serializers
from django.db.models import Count


def _get_news_papers(request, first):
    web_site = request.GET.get('web_site',None)
    timestring = request.GET.get('from',None) #timestring = "2005-09-01 12:30:09"
    time_format = "%Y-%m-%d %H:%M:%S"
    from_datetime = None
    if timestring:
        from_datetime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(timestring, time_format)))
        
    results = NewsPapers.objects.all()
    if web_site:
        results = results.filter(web_site=web_site)
    if from_datetime:
        results = results.filter(timestamp__gt=from_datetime)
    if first:
        
        num = int(first) * len(set([val['web_site'] for val in results.values('web_site')])) 
        results = results[:num]
        
    return results

def papers(request, first=None):
    results = _get_news_papers(request, first)
    data = serializers.serialize("json", results)
    return HttpResponse(data)

def head_lines(request, first=None):
    results = _get_news_papers(request, first)
    data = serializers.serialize("json", results, fields=('front_page_position','web_site','link','head_line', 'timestamp'))
    return HttpResponse(data)
    