# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem
from tutorial.polls.models import ProductModel, CategoryModel, ColorSizeModel

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):
    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        self.duplicates[spider] = set()

    def spider_closed(self, spider):
        print "Deleting duplicates set", len(self.duplicates[spider])
        del self.duplicates[spider]

    def process_item(self, item, spider):
        #print "In process_item", str(item), str(spider)
        if item['idx'] in self.duplicates[spider] or item['idx'] == -11111:
            raise DropItem("Duplicate/unparsed item found: %s" % item)
        else:
            self.duplicates[spider].add(item['idx'])
            return item
