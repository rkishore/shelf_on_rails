from django.db import models
from datetime import datetime

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
    
    #store = models.CharField(max_length=20, choices = STORE_CHOICES)
    store = models.ForeignKey('Brands', default='Nil')
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


class Brands(models.Model):
    name = models.CharField(max_length=200, default='Nil')

    def __unicode__(self):
        return self.name

class Items(models.Model):
    
    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('A', 'ALL'),
        )
    
    # These choices should be gender-specific                                                                                                                                  
    #MCAT_CHOICES = (
    #    ('Nil', 'Empty'),
    #    ('mens-dress-shirts', 'Dress-shirts'),
    #    ('mens-tees-and-tshirts', 'T-shirts'),
    #    ('mens-polo-shirts', 'Polo-shirts'),
    #    ('mens-shirts', 'Shirts'),
    #    ('mens-longsleeve-shirts', 'Longsleeve'),
    #    ('mens-shortsleeve-shirts', 'Shortsleeve'),
    #    ('mens-jackets', 'Jackets'),
    #    )

    # Each item is related to a single brand in the forward direction and                                                                                                      
    # each brand is related to many items in the reverse direction                                                                                                              
    brand = models.ForeignKey(Brands, default='Nil')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='A')
    cat1 = models.CharField(max_length=100, default='Nil')
    cat2 = models.CharField(max_length=100, default='Nil')
    cat3 = models.CharField(max_length=100, default='Nil')
    cat4 = models.CharField(max_length=100, default='Nil')
    cat5 = models.CharField(max_length=100, default='Nil')
    name = models.CharField(max_length=200, default='Nil')
    price = models.CharField(max_length=10, default='20.00')
    saleprice = models.CharField(max_length=10, default='10.00')
    insert_date = models.DateTimeField('Date inserted', default=datetime.now)
    #available_sizes = models.CharField(max_length=2, choices=SIZE_CHOICES)                                                                                                    
    #available_colors = models.CharField(max_length=2, choices=COLOR_CHOICES)                                                                                                   
    def __unicode__(self):
        return self.name
