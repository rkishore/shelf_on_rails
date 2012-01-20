from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from scrapy.http import Request
import re
from scrapy.exceptions import CloseSpider
import datetime 
import logging
import commands
from crawler.items import Category, ProductItem, ColorSizeItem, CategoryItem
from tutorial.polls.models import Brands, ProductModel
import os, errno
from time import sleep

logging.basicConfig(format='%(message)s', level=logging.CRITICAL)

class JCrewSpider(CrawlSpider):
    name = "jcrew"
    store_name = "J.Crew"
    HOME = "/Users/atulsingh/Documents/workspace2/"
    # stats
    all_items_scraped = set()
    count_scraped = 0
    urls_scraped = set()
    
    date = datetime.datetime.now()
    
    handle_httpstatus_list = [302]
    
    allowed_domains = ["jcrew.com"]
    #allowed_domains = ["express.com"]
    start_urls = [
        "http://www.jcrew.com/index.jsp"
        #"http://www.express.com/home.jsp"
    ]

    rules = (
    	     #Rule(SgmlLinkExtractor(allow=(r'index\.jsp$', ), unique=True), callback='parse_root', follow=True,
             #     process_request='avoid_redirection'),
             #Rule(SgmlLinkExtractor(allow=('http:\/\/www\.jcrew\.com\/[\w_]+\/[\w]+\.jsp',), unique=True), 
             #     callback='parse_sub', process_links='process_links_sub', follow=True,
             #     process_request='avoid_redirection'),
    	     #Rule(SgmlLinkExtractor(allow=('^http:\/\/www\.jcrew\.com\/[\w_]+\/[\w_]+\/[\w_]+\/[\w_\d~]+\/[\w_\d]+\.jsp$',), unique=True), 
             #     callback='parse_sub_sub', process_links='process_links_sub', follow=True, 
             #     process_request='avoid_redirection'),
             #Rule(SgmlLinkExtractor(allow=(r'http:\/\/www\.jcrew\.com\/',), unique=True), 
             #     callback='parse_sub_sub2', process_links='process_links_sub', follow=True, 
             #     process_request='avoid_redirection'),
             Rule(SgmlLinkExtractor(), 
                  callback='parse_sub_sub2', process_links='process_links_sub', follow=True, 
                  process_request='avoid_redirection'),           
            )

    # checks if tok is present in sub
    def _contains(self, sub, tok):
        index = sub.find(tok)
        if index >= 0:
            return True
        else:
            return False

    # combine the array elements into a single string with 
    # provided delimiters
    def _combine(self, string_array, start_delim, end_delim):
        result = ""
        for i in range(0, len(string_array)):
            result += start_delim
            result += string_array[i]
            result += end_delim
            
        return result
            
            
    def _create_dir(self, fpath):
        print "Creating directory: ", fpath
        
        try:
            os.makedirs(fpath)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST:
                pass
            else: raise
            
        
    def _store_in_file(self, response, item_id):
        path_name = self.HOME + "/" + str(self.date.isoformat())
        self._create_dir(path_name)
        path_name += "/" + self.store_name + "/"
        self._create_dir(path_name)
        
        fname = path_name + str(item_id) + ".html"
        FILE = open(fname, 'w')
        FILE.write(str(response.body))
        FILE.close()
        
        
        
    def parse_sub_sub2(self, response):
        #self._store_in_file(response, 0)
        # find category
        # find sub category
        url = response.url
        print "Parse_sub_sub2:: URL: " + str(url) + " Size of response: " + str(len(str(response.body)))
        if self._contains(str(url), 'PRD'):
            print "USEFUL URL " + str(url) 
            self.parse_sub_sub(response)
        return []
            
    def parse_sub_sub(self, response):
        hxs = HtmlXPathSelector(response)
        title_path = hxs.select('//title/text()').extract()
                
        self.count_scraped += 1
        
        
        ''' 
        PLAYING NICE: sleeping for 3min after crawling every 100 pages
        '''
        if self.count_scraped % 100 == 0:
            sleep(3*60) # sleep for 3 mins
            
        prod_url = response.url
        logging.critical("PRODUCT URL:" + str(prod_url) + " TITLE " + str(title_path))
        
        # find gender
        gender = 'M'
        if prod_url.find('women') >= 0 or prod_url.find('girl') >= 0:
            gender = 'F'
        logging.critical("Gender: " + gender)
        
        # find name of item
        item_name_path = hxs.select('//h1[contains (@class, "prodtitle")]/text()')
        item_name = item_name_path.extract()
        logging.critical("Name: " + str(item_name))
        
        '''
        TODO: if same page has multiple items, our logic will not work.
        So, leaving it for future.
        '''
        if len(item_name) == 0:
            logging.critical("DIDN'T FIND TITLE AT NORMAL PLACE, MUST BE SUIT. RETURNING." + str(prod_url))
            print item_name_path
            print "Size of response " + str(len(str(response)))
            print str(response)
            return []
        
        # find price and sale price
        item_id_, price_, sale_price_ = self._find_price(hxs)
        
        logging.critical("ITEM_ID " + str(item_id_) + " PRICE " + str(price_) + " SALE PRICE " + str(sale_price_))
        if price_ > sale_price_:
            logging.critical("SALE on ITEM_ID " + str(item_id_) + " PRICE " + str(price_) + " SALE PRICE " + str(sale_price_))
        # extract image URL
        prod_img_path = hxs.select('//div[contains (@class, "prod_main_img")]/a/img[contains (@src, "http")]/@src')
        prod_img_url = prod_img_path.extract()
        logging.critical("Image URL: " + str(prod_img_url))

        product = self._create_product_item(item_name[0], int(item_id_), str(prod_url), price_, \
                                            sale_price_, gender, str(prod_img_url[0]))
        # find colors available
        color_path = hxs.select('//select[contains (@onchange, "color")]/option/text()')
        colors = color_path.extract()
        logging.critical("Colors: " + str(colors[1:len(colors)]))
        
        
        # find sizes available        
        size_path = hxs.select('//select[contains (@onchange, "size")]/option/text()')
        sizes = size_path.extract()
        logging.debug("Sizes: " + str(sizes[1:len(sizes)]))
        
        self._create_color_size(product, colors[1:len(colors)], sizes[1:len(sizes)])
        
        # find category
        categories = prod_url.split('/')
        num_categories = len(categories)
        for i in range(3, num_categories - 2):
            logging.critical("Categories: " + categories[i])
        
        self._create_category(product, categories[3:num_categories-2])
        
        
        self._store_in_file(response, item_id_)
        #raise CloseSpider('Blah')
        logging.critical("Total unique items: " + str(len(self.all_items_scraped)) + " we have scraped so far: " +\
                          str(self.count_scraped) + " Unique URLs scraped: " + str(len(self.urls_scraped)))
        #raise SystemExit
        
        return []
        
    def process_links_sub(self, links):
        # we avoid links that are un-necessary or wrong
        # for J.Crew
        result = set()
        for l in links:
            url = str(l.url)
            if self._contains(url, 'catalog') or self._contains(url, 'help') or self._contains(url, 'footer') or self._contains(url, 'browse') or self._contains(url, 'search') or self._contains(url, 'include') or self._contains(url, 'footie'):
                continue
            else:
                result.add(l)
            
        return result
		
  
    def avoid_redirection(self, request):
        request.meta.update(dont_redirect=True)
        request.meta.update(dont_filter=True)
        return request
    
    def _create_product_item(self, name, prod_id, prod_url, price, saleprice, gender, img_url):
        item = ProductItem()
         
        b = Brands.objects.get(name = self.store_name)
        logging.critical("CREATE_PRODUCT OBJ: foreign key " + str(b))
        print "Prod id " + str(prod_id) + " url " + str(prod_url) + " img " + str(img_url)
        item['brand'] = b
        item['idx'] = prod_id
        item['name'] = name
        item['prod_url'] = prod_url
        item['price'] = price
        item['saleprice'] = saleprice
        item['promo_text'] = "None"
        item['err_text'] = "None"
        item['gender'] = gender
        item['img_url'] = img_url
        #print item
        
        return item.save()
        
    
    def _create_color_size(self, product, color_array, size_array):
        c_size = len(color_array)
        s_size = len(size_array)
        # pick the minimum
        min = c_size
        if c_size > s_size:
            min = s_size
        for i in range(0, min):
            colorsize = ColorSizeItem()
            colorsize['product'] = ProductModel.objects.get(pk=product.id)
            colorsize['color'] = color_array[i]
            colorsize['size'] = size_array[i]
            colorsize.save()
        
        
    
    def _create_category(self, product, categories):
        for cat in categories:
            category = CategoryItem()
            category['product'] = ProductModel.objects.get(pk=product.id)
            category['categoryId'] = 0
            category['categoryName'] = cat
            category.save()

    def _find_price(self, hxs):

        price_path = hxs.select('//td[@class="standard_nopad"]/text() | //td/font[@color="red"]/text()')
        _expr = '[\$]*[\d,]+[\.\d]*'
        _regex = re.compile(_expr)
        _list = price_path.re(_regex)
        logging.critical(_list)
        
        price = float(_list[0].strip('$').replace(',', ''))
        sale_price = price
        item_id = _list[1]
        if self._contains(_list[1], '$'):
            sale_price = float(_list[1].strip('$').replace(',',''))
            item_id = _list[2]

        return (item_id, price, sale_price)
        
        
        
        '''
        NOT USED RIGHT NOW
        '''
        # now get item_id and price from this 
        # the price is the base price without sale
        item_id = []
        price = []
        sale_price = []

        for item in items_u:
            if self._contains(item, '$'):
                item2 = item.strip('$').replace(',', '')
                price.append(item2)
                sale_price.append(item2)
            else:
                item_id.append(item)
                self.all_items_scraped.add(item)

            
        # this array contains the current price of the item
        # and associated item_id
        # using both these arrays, we can figure out if an item is on sale
        item_options_path = hxs.select('//input[contains (@onclick, "send")]')
        item_options = item_options_path.extract()
        selection_exp = '[\d]+[,\.\d]*'
        selection_regex = re.compile(selection_exp)
        selections_u = item_options_path.re(selection_regex)
        num_selections = len(selections_u)/4
        
        
        logging.critical("Selections: " + str(selections_u) + " size " + str(len(selections_u)/4) + " sale_price size " + str(len(sale_price)))
        
        item_id_selection = []

        # first element = item_id, second_element = price        
        for j in range(0, num_selections):
            slot = j*4
            logging.critical("Index: " + str(j) + " slot " + str(slot) + " len(selections_u) " + str(len(selections_u)))
            item_id_selection.append(selections_u[slot])
            sale_price[j] = selections_u[slot +1]
        
        for j in range(0, len(sale_price)):
            logging.critical("Price: " + str(price[j]) + " Sale Price " + str(sale_price[j]) + " Item " + str(item_id[j]))
