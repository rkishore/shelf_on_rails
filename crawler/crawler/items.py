# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from tutorial.polls.models import ProductModel, CategoryModel, ColorSizeModel

class CrawlerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class ProductItem(DjangoItem):
    django_model = ProductModel

class CategoryItem(DjangoItem):
    django_model = CategoryModel
    
class ColorSizeItem(DjangoItem):
    django_model = ColorSizeModel