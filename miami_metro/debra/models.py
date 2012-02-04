from django.db import models
from django.db.models import F
from django.forms import ModelForm
from datetime import datetime

# Create your models here.    
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
    
    #store = models.CharField(max_length=10, choices = STORE_CHOICES)
    store = models.ForeignKey('Brands', default='1')
    d = models.DateField('date issued')
    #d_expire = models.DateField('expiry date')
    validity = models.IntegerField(default=0)
    code = models.CharField(max_length=20)
    where_avail = models.IntegerField(choices= AVAILABILITY_CHOICES, default=0)
    free_shipping_lower_bound = models.IntegerField(default=10000)
    
    PROMO_TYPE_CHOICES = (
                          (0, 'STORE-WIDE'),
                          (1, 'AGGREGATE'),
                          (2, 'ADDITIONAL'),
                          (3, 'BUY-1-GET'),
                          (4, 'BUY-N-FOR')
                          )
    
    promo_type = models.IntegerField(choices = PROMO_TYPE_CHOICES, default=0)
    
    promo_disc_perc = models.IntegerField(default=0)
    promo_disc_amount = models.IntegerField(default=0)
    promo_disc_lower_bound = models.IntegerField(default=0)
    
    SEX_CHOICES = (
                   (0, 'MALE'),
                   (1, 'FEMALE'),
                   (2, 'ALL'),
                   )
    sex_category = models.IntegerField(choices = SEX_CHOICES, default=0)
    
    ITEM_CATEGORY_CHOICES = (
                             (0, 'SHIRTS'),
                             (1, 'PANTS'),
                             (2, 'SWEATERS'),
                             (3, 'JEANS'),
                             (4, 'OUTERWEAR'),
                             (5, 'UNDERWEAR'),
                             (7, 'EVERYTHING')
                             )
    
    item_category = models.IntegerField(choices = ITEM_CATEGORY_CHOICES, default=0)
    
    class Meta:
        unique_together = ('store', 'd', 'promo_type', 'promo_disc_perc', 'promo_disc_amount',
                           'promo_disc_lower_bound', 'sex_category', 'item_category')


    def __unicode__(self):
        return str(self.store) + " " + str(self.d) + " " + str(self.promo_type)  


class Brands(models.Model):
    name = models.CharField(max_length=200, default='Nil')
    def __unicode__(self):
        return self.name

class Items(models.Model):
    
    # Each item is related to a single brand in the forward direction and                                                                                                      
    # each brand is related to many items in the reverse direction                                                                                                             
    
    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('A', 'ALL'),
        ('O', 'OTHER'),
        )
 
    brand = models.ForeignKey(Brands, default='1')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='A')
    cat1 = models.CharField(max_length=100, default='Nil')
    cat2 = models.CharField(max_length=100, default='Nil')
    cat3 = models.CharField(max_length=100, default='Nil')
    cat4 = models.CharField(max_length=100, default='Nil')
    cat5 = models.CharField(max_length=100, default='Nil')
    name = models.CharField(max_length=200, default='Nil')
    price = models.FloatField(max_length=10, default='20.00')
    saleprice = models.FloatField(max_length=10, default='10.00')
    insert_date = models.DateTimeField('Date inserted', default=datetime.now)
    img_url_sm = models.CharField(max_length=200, default='Nil')
    img_url_md = models.CharField(max_length=200, default='Nil')
    img_url_lg = models.CharField(max_length=200, default='Nil')
    pr_url = models.CharField(max_length=200, default='Nil')
    pr_sizes = models.CharField(max_length=600, default='Nil')
    pr_colors = models.CharField(max_length=600, default='Nil')
    pr_instock = models.CharField(max_length=10, default='Nil')
    pr_retailer = models.CharField(max_length=200, default='Nil')
    pr_currency = models.CharField(max_length=200, default='Nil')
    product_model_key = models.OneToOneField('ProductModel', blank=True, null=True)
                                                                                                           
    def __unicode__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=100, default='Nil')
    brand = models.ManyToManyField(Brands)
    
    def __unicode__(self):
        #return u'%s %s' % (self.name, self.brand)
        return self.name

    
class SSItemStats(models.Model):
    '''
    Here we store the statistics on a (brand, category, gender, date, price_selection_criteria) basis for items from the SS catalog. 
    SELECTION_METRICS is used to select items from the Items DB
    using the specific criteria: do we want to use the cheapest (Min)
    or most expensive (Max) or average (Median)
    '''
    SELECTION_METRICS = (
        (0, 'AVERAGE'),
        (1, 'MAXIMUM'),
        (2, 'MINIMUM'),
        (3, 'MEDIAN'),
        (4, 'Q75'),
        (5, 'Q25'),                         
        )

    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('A', 'ALL'),
        )

    tdate = models.DateField('Date generated', default=datetime.now())
    brand = models.ForeignKey(Brands, default='1')
    category = models.CharField(max_length=10, default='Nil')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='A')
    price_selection_metric = models.IntegerField(choices = SELECTION_METRICS, default=0)
    price = models.FloatField(max_length=10, default='-111.00')
    saleprice = models.FloatField(max_length=10, default='-111.00')
    total_cnt = models.IntegerField(max_length=10, default='-11')
    sale_cnt = models.IntegerField(max_length=10, default='-11')
    
    def __unicode__(self):
        return "SSItemStats: " + str(self.tdate) + " brand: " + str(self.brand.name) + " category: " + \
                str(self.category) + " gender: " + str(self.gender) + " selection_metric: " + \
                str(self.price_selection_metric)
    
class ProductModel(models.Model):
    ''' 
    This model holds the items scraped by our spiders
    '''
    brand = models.ForeignKey(Brands, default='1')
    idx = models.IntegerField(max_length=10, default='-11')
    name = models.CharField(max_length=200, default='Nil')
    prod_url = models.URLField(verify_exists=False, default='Nil')
    price = models.FloatField(max_length=10, default='-11.0')
    saleprice = models.FloatField(max_length=10, default='-11.0')
    promo_text = models.CharField(max_length=200, default='Nil')
    err_text = models.CharField(max_length=200, default='Nil')
    gender = models.CharField(max_length=6, default='Nil')
    img_url = models.URLField(verify_exists=False, default='Nil')
    description = models.TextField(default='Nil')
    insert_date = models.DateTimeField('Date inserted', default=datetime.now)

    def __unicode__(self):
        return u'%s: %d %s' % (self.brand.name, self.idx, self.name)


class ColorSizeModel(models.Model):
    ''' 
    This model holds the color and size information for the products scraped by our spiders.
    We have one column for each color and size combination for each product.
    '''
    product = models.ForeignKey(ProductModel, default='0') 
    color = models.CharField(max_length=50, default='Nil')
    size = models.CharField(max_length=50, default='Nil')

    def __unicode__(self):
        return u'%s: %d %s %s %s' % (self.product.brand.name, self.product.idx, self.product.name, self.color, self.size)

class CategoryModel(models.Model):
    ''' 
    This model holds the category information for the products scraped by our spiders.
    We have one column for each category that a product belongs to.
    '''
    product = models.ForeignKey(ProductModel, default='0') 
    categoryId = models.IntegerField(max_length=50, default='-111')
    categoryName = models.CharField(max_length=100, default='Nil')
    
    def __unicode__(self):
        return u'%s: %d %s %s' % (self.product.brand.name, self.product.idx, self.product.name, self.categoryName)
        
class UserIdMap(models.Model):
    ip_addr = models.CharField(max_length=50, default='-11.11.11.11')
    user_id = models.IntegerField(max_length=50, default='-1111')
    
    def __unicode__(self):
        return u'%s %d' % (str(self.ip_addr), int(self.user_id))
    
class WishlistI(models.Model):
    user_id = models.ForeignKey(UserIdMap, default='0')
    color = models.CharField(max_length=100, blank=True, null=True, default='Nil')
    size = models.CharField(max_length=100, blank=True, null=True, default='Nil')
    quantity = models.IntegerField(max_length=50, blank=True, null=True, default='-1')
    img_url = models.URLField(max_length=1000, default='Nil')
    item = models.ForeignKey(ProductModel, blank=True, null=True, default='0')
    
    def __unicode__(self):    
        #print self.user_id.user_id, self.item.idx, self.item.name 
        #return '%d %d %s' % (int(self.user_id.user_id), int(self.item.idx), str(self.item.name))
        return '%d %d %s %s %d' % (int(self.user_id.user_id), int(self.item.idx), str(self.color), str(self.size), int(self.quantity))    
    
class StoreItemCombinationResults(models.Model):
    '''
    This model stores the total price for a set of items. We store this in a DB
    to avoid re-calculating it again-and-again. combination_id is a sha-1 hash of
    item ids of items in the list. 
    '''
    combination_id = models.CharField(max_length=200, default='Nil')
    price = models.FloatField(max_length=10, default='-11.0')
    saleprice = models.FloatField(max_length=10, default='-11.0')
    free_shipping = models.BooleanField(default='False')

    def __unicode__(self):
        return "ItemComb: comb " + str(self.combination_id) + " price: " + str(self.price) + " sale " + str(self.saleprice)
