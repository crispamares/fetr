'''
Created on 24/06/2011

@author: crispamares
'''
from django_cron import cronScheduler, Job

# This is a function I wrote to check a feedback email address and add it to our database. Replace with your own imports
from models import feed_news_papers

class GetNews(Job):
        run_every = 1800 #(30 minutes)
                
        def job(self):
                # This will be executed every 5 minutes
                feed_news_papers()

cronScheduler.register(GetNews)