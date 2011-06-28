from django.db import models
from fetr_lib import crawler, keys

# Create your models here.
 
 
def feed_news_papers():
    errors = []
    c = crawler.Crawler()
    links = c.get_front_pages_links()
    papers = c.run(links, errors)
    
    for paper in papers:
        link = paper[1]
        paper_set = NewsPapers.objects.filter(link=link)

        if len(paper_set) > 1:
            Log(msg = "Two papers with the same link: "+ link, type_err ="DB ERROR").save()
        elif not paper_set.exists():     
            np = NewsPapers(web_site = paper[0],
                            link = paper[1],
                            head_line = paper[2],
                            text = paper[3],
                            front_page_position = paper[4] 
                            )
            np.save()
            #try:
            analizer = keys.NLAnalizer()
            nnp_keys = analizer.get_nnp(paper[3])
            for nnp_key in nnp_keys:   
                KeyWords(paper = np,
                         proper_noun = True,
                         word = nnp_key[0],
                         ocurrences = nnp_key[1]
                         ).save()
            freq_keys = analizer.extract_freq_keywords(paper[3])
            for f_key in freq_keys:   
                KeyWords(paper = np,
                         proper_noun = False,
                         word = f_key[0],
                         ocurrences = f_key[1]
                         ).save()

            #except:
            #    Log(msg = paper[1], type_err ="KeyWords Error").save()

        elif paper_set[0].head_line != paper[2]:
            print "Actualizo"
            paper_set[0].head_line = paper[2]
            paper_set[0].text = paper[3]
            paper_set[0].front_page_position = paper[4]
            paper_set[0].save()
            Log(msg = link, type_err ="Updating").save()
    if errors:
        for error in errors:
            Log(msg = error, type_err ="Error parsing").save()

 
class NewsPapers(models.Model):
    web_site = models.CharField(max_length=100)
    link = models.CharField(max_length=300)
    head_line = models.CharField(max_length=300)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=True)
    front_page_position = models.IntegerField() 
    
    def __unicode__(self):
        return u'%s' %(self.link)
    
    def natural_key(self):
        return self.link

    class Meta(object):
        ordering = ['front_page_position', '-timestamp']

    def last_first_paper(self):
        return [a.link for a in NewsPapers.objects.all() if a.front_page_position == 0].pop()
    
    @staticmethod
    def get_web_sites():
        return set([val['web_site'] for val in NewsPapers.objects.values('web_site')])

class KeyWords(models.Model):
    word = models.CharField(max_length=50)
    ocurrences = models.IntegerField()
    paper = models.ForeignKey(NewsPapers)
    proper_noun = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    def __unicode__(self):
        return u'%s' %(self.word)
    
    class Meta(object):
        ordering = ['-ocurrences']

class Log(models.Model):
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=True)
    msg = models.CharField(max_length=300)
    type_err = models.CharField(max_length=20)
    
    def __unicode__(self):
        return u'%s:%s, - %s' %(self.type_err, self.timestamp.isoformat(), self.msg)
