from django.db import models
from django.db.models import F
from django.forms import ModelForm
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
    #d_expire = models.DateField('expiry date')
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
        return str(self.store) + " " + str(self.d) + " " + str(self.promo_type)  


class Brands(models.Model):
    name = models.CharField(max_length=200, default='Nil')

    def __unicode__(self):
        return self.name

GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('A', 'ALL'),
        )

class Items(models.Model):
    
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
    price = models.FloatField(max_length=10, default='20.00')
    saleprice = models.FloatField(max_length=10, default='10.00')
    insert_date = models.DateTimeField('Date inserted', default=datetime.now)
    img_url_sm = models.CharField(max_length=200, default='Nil')
    img_url_md = models.CharField(max_length=200, default='Nil')
    img_url_lg = models.CharField(max_length=200, default='Nil')
    pr_url = models.CharField(max_length=200, default='Nil')
    pr_sizes = models.CharField(max_length=200, default='Nil')
    pr_colors = models.CharField(max_length=200, default='Nil')
    pr_instock = models.CharField(max_length=10, default='Nil')
    pr_retailer = models.CharField(max_length=200, default='Nil')
    pr_currency = models.CharField(max_length=200, default='Nil')
                                                                                                           
    def __unicode__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=100, default='Nil')
    brand = models.ManyToManyField(Brands)
    
    def __unicode__(self):
        #return u'%s %s' % (self.name, self.brand)
        return self.name

class Demand(models.Model):
    '''
    This model holds the demand object. We are going to store our analysis for 
    each demand in the DB.
    '''
    NUM_CHOICES = (
                   (0, 0),
                   (1, 1),
                   (2, 2),
                   (3, 3)
                   )
    
    GENDER_CHOICES = (
                      ('M', 'MALE'),
                      ('F', 'FEMALE'),
                      ('A', 'ALL'),
                      )
    num_shirts = models.IntegerField(choices = NUM_CHOICES)
    num_sweaters = models.IntegerField(choices = NUM_CHOICES)
    num_skirts = models.IntegerField(choices = NUM_CHOICES)
    num_jeans = models.IntegerField(choices = NUM_CHOICES)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='A')
    total_items = models.IntegerField()
    def __unicode__(self):
        return "Demand: Shirt: " + str(self.num_shirts) + " Sweaters: " + str(self.num_sweaters) + \
                " Skirts: " + str(self.num_skirts) + " Jeans: " + str(self.num_jeans) + " Gender: " + \
                str(self.gender)
    
class ItemList(models.Model):
    ''' 
    This model holds the items that satisfy the demand
    related_name field is required since we have multiple fields in this
    model that have same ForeignKey class: item.
    Django automatically creates a reverse-mapping from Items model to this
    ItemList model. For each item in the Items table, there will be a manager
    called item.itemlist_set which can be used to find all itemlist objects that
    have a given item. However, since we have multiple items in the itemlist table,
    django gets confused about what name to give each. Thus, we provide a related_name
    to disambiguate this.
    '''
    item1 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist1")
    item2 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist2")    
    item3 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist3")    
    item4 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist4")    
    item5 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist5")    
    item6 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist6")    
    item7 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist7")    
    item8 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist8")    
    item9 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist9")    
    item10 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist10")    
    item11 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist11")    
    item12 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist12")    
    item13 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist13")    
    item14 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist14")    
    item15 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist15")    
    item16 = models.ForeignKey(Items, blank=True, null=True, default='Nil', related_name = "itemlist16")
    total_items = models.IntegerField(default='0')
    
    def __unicode__(self):
        return "ItemList size: " + str(self.total_items)
    
class ResultForDemand(models.Model):
    '''
    Here we store the results for the demands. 
    SELECTION_METRICS is used to select items from the Items DB
    using the specific criteria: do we want to use the cheapest (Min)
    or most expensive (Max) or average (Median)
    '''
    SELECTION_METRICS = (
                         (0, 'MINIMUM'),
                         (1, 'MAXIMUM'),
                         (2, 'MEDIAN'),
                         (3, 'RANDOM'),
                         (4, 'USER'),                         
                         )
    demand = models.ForeignKey(Demand, blank=True, null=True, default='Nil')
    date = models.DateField('Date generated', default=datetime.now())
    itemlist = models.ForeignKey(ItemList, blank=True, null=True, default='Nil')
    total_without_sale = models.FloatField(max_length=10, default='10.00')
    total_with_sale = models.FloatField(max_length=10, default='10.00')
    free_shipping = models.BooleanField(default='False')
    store_name = models.ForeignKey(Brands, blank=True, null=True, default='Nil')
    store_string = models.CharField(max_length = 10, default='Nil')
    item_selection_metric = models.IntegerField(choices = SELECTION_METRICS, default='0')
    
    
    def __unicode__(self):
        return "ResultForDemand: " + str(self.date) + " store: " + str(self.store_string) + " selection_metric: " + \
                str(self.item_selection_metric)
    
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
    tdate = models.DateField('Date generated', default=datetime.now())
    brand = models.ForeignKey(Brands, default='Nil')
    category = models.CharField(max_length=20, default='Nil')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='A')
    price_selection_metric = models.IntegerField(choices = SELECTION_METRICS, default='0')
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
    brand = models.ForeignKey(Brands, default='Nil')
    idx = models.IntegerField(max_length=10, default='Nil')
    name = models.CharField(max_length=200, default='Nil')
    prod_url = models.URLField(verify_exists=False, default='Nil')
    price = models.FloatField(max_length=10, default='Nil')
    saleprice = models.FloatField(max_length=10, default='Nil')
    promo_text = models.CharField(max_length=200, default='Nil')
    err_text = models.CharField(max_length=200, default='Nil')
    gender = models.CharField(max_length=6, default='Nil')
    img_url = models.URLField(verify_exists=False, default='Nil')

    def __unicode__(self):
        return u'%s: %d %s' % (self.brand.name, self.idx, self.name)


class ColorSizeModel(models.Model):
    ''' 
    This model holds the color and size information for the products scraped by our spiders.
    We have one column for each color and size combination for each product.
    '''
    product = models.ForeignKey(ProductModel, default='Nil') 
    color = models.CharField(max_length=50, default='Nil')
    size = models.CharField(max_length=50, default='Nil')

    def __unicode__(self):
        return u'%s: %d %s %s %s' % (self.product.brand.name, self.product.idx, self.product.name, self.color, self.size)

class CategoryModel(models.Model):
    ''' 
    This model holds the category information for the products scraped by our spiders.
    We have one column for each category that a product belongs to.
    '''
    product = models.ForeignKey(ProductModel, default='Nil') 
    categoryId = models.IntegerField(max_length=50, default='Nil')
    categoryName = models.CharField(max_length=50, default='Nil')
    
    def __unicode__(self):
        return u'%s: %d %s %s' % (self.product.brand.name, self.product.idx, self.product.name, self.categoryName)
        
class UserIdMap(models.Model):
    ip_addr = models.CharField(max_length=50, default='-11.11.11.11')
    user_id = models.IntegerField(max_length=50, default='-1111')
    
    def __unicode__(self):
        return u'%s %d' % (str(self.ip_addr), int(self.user_id))
    
class WishlistI(models.Model):
    #user_id = models.IntegerField(max_length=50, default='-1111')
    user_id = models.ForeignKey(UserIdMap, default='Nil')
    item = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil')
    
    def __unicode__(self):
        print self.user_id.user_id, self.item.idx, self.item.name 
        #return '%d %d %s' % (int(self.user_id.user_id), int(self.item.idx), str(self.item.name))
        return '%d %d' % (int(self.user_id.user_id), int(self.item.idx))

class WishlistM(models.Model):
    #user_id = models.IntegerField(max_length=50, default='-1111')
    item1 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist1")
    item2 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist2")    
    item3 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist3")    
    item4 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist4")    
    item5 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist5")    
    item6 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist6")    
    item7 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist7")    
    item8 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist8")    
    item9 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist9")    
    item10 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist10")    
    item11 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist11")    
    item12 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist12")    
    item13 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist13")    
    item14 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist14")    
    item15 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist15")    
    item16 = models.ForeignKey(ProductModel, blank=True, null=True, default='Nil', related_name = "prodlist16")
    total_prods = models.IntegerField(default='0')
    
    def __unicode__(self):
        return "ProdList size: " + str(self.total_prods)
    
    
class StoreItemCombinationResults(models.Model):
    '''
    This model stores the total price for a set of items. We store this in a DB
    to avoid re-calculating it again-and-again. combination_id is a sha-1 hash of
    item ids of items in the list. 
    '''
    combination_id = models.CharField(max_length=200, default='Nil')
    price = models.FloatField(max_length=10, default='Nil')
    saleprice = models.FloatField(max_length=10, default='Nil')
    free_shipping = models.BooleanField(default='False')

    def __unicode__(self):
        return "ItemComb: comb " + str(combination_id) + " price: " + str(price) + " sale " + str(saleprice)
