# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

from scrapy.contrib_exp.djangoitem import DjangoItem 
from tutorial.polls.models import ProductModel, CategoryModel, ColorSizeModel

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


class Category(Item):

    name = Field()
    url = Field()
    
    def __str__(self):
        return "Category: name=%s url=%s" % (self['name'], self['url'])
    
class ProductItem(DjangoItem):
    django_model = ProductModel

class CategoryItem(DjangoItem):
    django_model = CategoryModel
    
class ColorSizeItem(DjangoItem):
    django_model = ColorSizeModel
