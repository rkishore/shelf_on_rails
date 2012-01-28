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
import copy

logging.basicConfig(format='%(message)s', level=logging.CRITICAL)

class ExpressSpider(CrawlSpider):
    name = "express"
    store_name = "Express"
    HOME = "/Users/atulsingh/Documents/workspace2/"
    # stats
    all_items_scraped = set()
    count_scraped = 0
    urls_scraped = set()
    items_to_scrape = []
    items_scraped = []
    count = 0
    date = datetime.datetime.now()
    
    handle_httpstatus_list = [302]
    
    allowed_domains = ["express.com"]
    #allowed_domains = ["express.com"]
    start_urls = [
        "http://www.express.com/home.jsp"
        #"http://www.express.com/1mx-shirts-800/control/show/12/index.cat"
    ]

    rules = (
             Rule(SgmlLinkExtractor(restrict_xpaths=('//td[@class="cat-glo-page-action"]//a[.="next"]',)), 
                  callback='parse_sub_sub2', 
                  process_links='process_links_sub', follow=True, 
                  process_request='avoid_redirection'),
             Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="header-top"]',)), 
                  callback='parse_sub_sub2', 
                  process_links='process_links_sub', follow=True, 
                  process_request='avoid_redirection'),
             Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="cat-thu-row cat-thu-row-all"] | //div[@class="cat-thu-row cat-thu-row-all"]',)), 
                  callback='parse_sub_sub2', process_links='process_links_sub', follow=True, 
                  process_request='avoid_redirection'),
             Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@id="glo-leftnav-container"]',)), 
                  callback='parse_sub_sub2', 
                  process_links='process_links_sub', follow=True, 
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
        print "Parse_sub_sub2:: " + str(self.count) + " URL: " + str(url) + " Size of response: " + str(len(str(response.body)))
        if self._contains(str(url), '/index.pro'):
            print "USEFUL URL " + str(url) 
            self.parse_sub_sub(response)
            
        self.count += 1
        return []
            
    def parse_sub_sub(self, response):
        hxs = HtmlXPathSelector(response)
        title_path = hxs.select('//title/text()').extract()
        
        
                
        self.count_scraped += 1
        
        ''' 
        PLAYING NICE: sleeping for 1min after crawling every 100 pages
        '''
        if self.count_scraped % 100 == 0:
            sleep(0) # sleep for 1 mins for express
            
        prod_url = response.url
        logging.critical("PRODUCT URL:" + str(prod_url) + " TITLE " + str(title_path) + " TOTAL SO FAR " + str(self.count_scraped))

        # find gender
        gender = 'M'
        if prod_url.lower().find('women') >= 0 or prod_url.lower().find('girl') >= 0:
            gender = 'F'
        logging.critical("Gender: " + gender)
        
        # find name of item
        item_name_path = hxs.select('//div[@id="cat-pro-con-detail"]//h1/text()')
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
        item_id_, price_, sale_price_ = self._find_price(hxs, prod_url)
        
        if item_id_ in self.items_scraped:
            logging.critical("ITEM ALREADY SCRAPED " + str(item_id_) + ". RETURNING.")
            return
        else:
            self.items_scraped.append(item_id_)
            
        logging.critical("ITEM_ID " + str(item_id_) + " PRICE " + str(price_) + " SALE PRICE " + str(sale_price_))
        if price_ > sale_price_:
            logging.critical("SALE on ITEM_ID " + str(item_id_) + " PRICE " + str(price_) + " SALE PRICE " + str(sale_price_))
        
        
        # extract image URL
        prod_img_path = hxs.select('//link[@rel="image_src"]')
        prod_img_str = str(prod_img_path.extract()[0])
        prod_img_url = prod_img_str[28: len(prod_img_str) - 2]
        logging.critical("Image URL: " + str(prod_img_url))

        product = self._create_product_item(item_name[0], int(item_id_), str(prod_url), price_, \
                                            sale_price_, gender, str(prod_img_url[0]))
        
        # find colors available
        colorSizeMapping = self._get_color_size_array(response)
        logging.critical(colorSizeMapping)
        
        #self._create_color_size(product, colors[1:len(colors)], sizes[1:len(sizes)])
        
        # find category
        categories = prod_url.split('/')
        num_categories = len(categories)
        for i in range(3, num_categories - 2):
            logging.critical("Categories: " + categories[i])
        
        self._create_category(product, categories[3:num_categories-2])
        
        # find description and keywords: these will be useful in categorization
        desc = hxs.select('//div[@id="cat-pro-con-detail"]//li[@class="cat-pro-desc"]/text()').extract()
        logging.critical("Description: " + str(desc))
        
        # promo text
        promo_path = hxs.select('//span[@class="cat-pro-promo-text"]//font/text()').extract()
        promo_str = str(promo_path)
        logging.critical("Promotion:" + promo_str)
        
        
        #self._store_in_file(response, item_id_)
        #raise CloseSpider('Blah')
        logging.critical("Total unique items: " + str(len(self.all_items_scraped)) + " we have scraped so far: " +\
                          str(self.count_scraped) + " Unique URLs scraped: " + str(len(self.urls_scraped)))
        #raise SystemExit
        
        return []
        
        
    def process_links_none(self, links):
        print "Links from BVReviews: " + str(links)
        return set()
    
    def process_links_sub(self, links):
        return links
		
    def find_itemid_in_url(self, url_str):
        end = url_str.rfind('-')
        s1 = url_str[0:end]
        start = s1.rfind('-')
        itemid = s1[start+1: len(s1)]
        #print itemid
        #raise SystemExit
        return itemid


  
    def avoid_redirection(self, request):
        request.meta.update(dont_redirect=True)
        #request.meta.update(dont_filter=True)
        return request
    
    def _get_color_size_array(self, response):
        colorToSizeArray = re.findall('colorToSize[\w\d\[\]\\\',=\s]+;', str(response.body))
        #print colorToSizeArray
        total = len(colorToSizeArray)
        colorSizeMapping = {}
        
        for i in range(0, total):
            mapping_var = colorToSizeArray[i]
            #print mapping_var
            '''
            mapping_var is a string, e.g.: colorToSize42466Array['ENSIGN'] = ['X Small', 'Small', 'Large'];
            '''
            square_brk_left = mapping_var.find('[')
            square_brk_right = mapping_var.find(']')
            #print "Square_left " + str(square_brk_left) + " Square_right " + str(square_brk_right)
            color = mapping_var[square_brk_left+2: square_brk_right-1]
            #print color
            
            sizes_str = mapping_var[square_brk_right+5: len(mapping_var)]
            #print sizes_str
            
            num_sizes = sizes_str.count(',') + 1
            #print "Num sizes " + str(num_sizes)
            size = []
            for j in range(0, num_sizes):
                single_quote_left = sizes_str.find("\'")
                #print "Quoteleft " + str(single_quote_left)
                remaining_sizes_str = sizes_str[single_quote_left+1: len(sizes_str)]
                #print "Remaining " + remaining_sizes_str
                single_quote_right = remaining_sizes_str.find("\'")
                #print "QuoteRight " + str(single_quote_right)
                size_elem = remaining_sizes_str[0: single_quote_right]
                #print "Size_elem " + size_elem
                size.append(size_elem)
                sizes_str = sizes_str[single_quote_right+ single_quote_left + 3: len(sizes_str)]
            #print size
            colorSizeMapping[color] = copy.deepcopy(size)
    
        return colorSizeMapping
    
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

    def _find_price(self, hxs, url):
        item_id = self.find_itemid_in_url(url)
        price_path = hxs.select('//li[@class="cat-pro-price"]//span//text() | //li[@class="cat-pro-price"]//strong//text()')
        _list = price_path.extract()
        logging.critical(_list)
        
        '''
        Some items have their prices given in a range: $30-$45. The price can be a function of
        size or style. We currently only store the minimal size.
        '''
        
        if self._contains(_list[0], '-'):
            loc = _list[0].find('-')
            new_ = _list[0][0:loc]
            price = float(new_.strip('$').replace('\n', '').replace('\t', ''))
            #print "Price: " + str(price) + " orig " + str(_list[0])
            #raise SystemExit
        else:
            price = float(_list[0].strip('$').replace('\n', '').replace('\t', ''))

        sale_price = price
        if len(_list) > 1:
            if self._contains(_list[1], '-'):
                loc = _list[1].find('-')
                new_ = _list[1][0:loc]
                sale_price = float(new_.strip('$').replace('\n', '').replace('\t', ''))
            else:
                sale_price = float(_list[1].strip('$').replace('\n','').replace('\t', ''))
    
        return (item_id, price, sale_price)
        
        
        
        