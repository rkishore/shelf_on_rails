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
    
    

    

class Promoinfo(models.Model):
    
    STORE_CHOICES = (
                     ('JCREW', 'JCREW'),
                     ('EXPRESS', 'EXPRESS'),
                     )
    
    AVAILABILITY_CHOICES = (
                        (0, 'STORES ONLY'),
                        (1, 'ONLINE ONLY'),
                        (2, 'BOTH')
                        )
    
    store = models.CharField(max_length=20, choices = STORE_CHOICES)
    d = models.DateField('date issued')
    validity = models.IntegerField()
    code = models.CharField(max_length=20)
    where_avail = models.IntegerField(choices= AVAILABILITY_CHOICES)
    free_shipping_lower_bound = models.IntegerField()
    
    PROMO_TYPE_CHOICES = (
                          (0, 'STORE-WIDE'),
                          (1, 'AGGREGATE'),
                          (2, 'ADDITIONAL'),
                          (3, 'BUY-1-GET'),
                          (4, 'BUY-N-FOR')
                          )
    
    promo_type = models.IntegerField(choices = PROMO_TYPE_CHOICES)
    
    promo_disc_perc = models.IntegerField()
    promo_disc_amount = models.IntegerField()
    promo_disc_lower_bound = models.IntegerField()
    
    SEX_CHOICES = (
                   (0, 'MALE'),
                   (1, 'FEMALE'),
                   (2, 'ALL'),
                   )
    sex_category = models.IntegerField(choices = SEX_CHOICES)
    
    ITEM_CATEGORY_CHOICES = (
                             (0, 'SHIRTS'),
                             (1, 'PANTS'),
                             (2, 'SWEATERS'),
                             (3, 'JEANS'),
                             (4, 'OUTERWEAR'),
                             (5, 'UNDERWEAR'),
                             (7, 'EVERYTHING')
                             )
    
    item_category = models.IntegerField(choices = ITEM_CATEGORY_CHOICES)
    
    class Meta:
        unique_together = ('store', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount',
                           'promo_disc_lower_bound', 'sex_category', 'item_category')


    def __unicode__(self):
        return self.store + " " + str(self.d) + " " + str(self.promo_type)  