# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib_exp.djangoitem import DjangoItem
from tutorial.polls.models import Items

class CrawlerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    prod_name = Field()
    store_name = Field()
    date_inserted = Field()
    prod_url = Field()
    img_url = Field()
    categories = Field()
    sizes = Field()
    color = Field()
    price = Field()
    saleprice = Field()
    gender = Field()
    
    pass

class ProductItem(DjangoItem):
    django_model = Items