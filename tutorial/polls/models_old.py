from django.db import models

# Create your models here.


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.question
    
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    
    def __unicode__(self):
        return self.choice
    
    
    
class Promotion(models.Model):
    store = models.CharField(max_length=200)
    issued = models.DateField('date issued')
    validity = models.IntegerField()
    code = models.CharField(max_length=8)
    where_avail = models.IntegerField()
    shipping = models.IntegerField()
    promo_type = models.IntegerField()
       
    disc_perc = models.IntegerField()
    disc_aggr_amount = models.IntegerField()
    disc_aggr_low_bound = models.IntegerField()
    disc_add_perc = models.IntegerField()
    
    sex_category = models.IntegerField()
    item_category = models.IntegerField()
    
