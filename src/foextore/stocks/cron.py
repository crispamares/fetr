'''
Created on 24/06/2011

@author: crispamares
'''
from django_cron import cronScheduler, Job

# This is a function I wrote to check a feedback email address and add it to our database. Replace with your own imports
from models import feed_stocks

class GetStocks(Job):
        """
                Cron Job that checks the lgr users mailbox and adds any approved senders' attachments to the db
        """

        # run every 60 seconds (1 minute)
        run_every = 45
                
        def job(self):
                # This will be executed every 5 minutes
                feed_stocks()

cronScheduler.register(GetStocks)