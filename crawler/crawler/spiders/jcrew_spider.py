from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from scrapy.http import Request
import re
from scrapy.exceptions import CloseSpider
import datetime 

class JCrewSpider(CrawlSpider):
    name = "jcrew"
    allowed_domains = ["jcrew.com"]
    start_urls = [
        "http://www.jcrew.com/index.jsp"
    ]

    rules = (
    	     Rule(SgmlLinkExtractor(allow=(r'index\.jsp$', ), unique=True), callback='parse_root', follow=True,
                  process_request='avoid_redirection'),
             #Rule(SgmlLinkExtractor(allow=('^http:\/\/www\.jcrew\.com\/include\/empty\.jsp[\w\d\.?%=&]*',), unique=True), 
             #     process_links='process_links_avoid', callback='parse_exclude_for_testing', follow=True),
             Rule(SgmlLinkExtractor(allow=('^http:\/\/www\.jcrew\.com\/mens_category\/[\w]+\.jsp$',), unique=True), 
                  callback='parse_sub', process_links='process_links_sub', follow=True,
                  process_request='avoid_redirection'),
    	     #Rule(SgmlLinkExtractor(allow=('^http:\/\/www\.jcrew\.com\/[\w_]+\/[\w_]+\/[\w_]+\/[\w_\d~]+\/[\w_\d]+\.jsp$',), unique=True), 
             #    callback='parse_sub_sub', process_links='process_links_sub', follow=True),        
             Rule(SgmlLinkExtractor(allow=('^http:\/\/www\.jcrew\.com\/mens_category\/[\w_]+\/[\w_]+\/[\w_\d~]+\/[\w_\d]+\.jsp$',), unique=True), 
                  callback='parse_sub_sub', process_links='process_links_sub', follow=True, 
                  process_request='avoid_redirection'),        
            
            )

    def print_list(self, res, level):
    	for l in res:
    		print "GOT THIS AT " + str(level) + " " + str(l)
   
            
    def parse_root(self, response):
    	hxs = HtmlXPathSelector(response)
    	res = hxs.select('//tr/td/a[contains (@href,"http")]/@href').extract()	
    	self.print_list(res, "ROOT")
    	return []

    def parse_sub(self, response):
    	hxs = HtmlXPathSelector(response)
        s1 = hxs.select('//tr/td[contains (@class,"subCategory")]')
        s2 = s1.select('//a[contains(@href, "http")]/@href')
        res = s2.extract()
       	#self.print_list(res, "SUB-ROOT")
       	print "HELLO SUB: " + str(response.url)
        return []

    def parse_sub_sub(self, response):
        hxs = HtmlXPathSelector(response)
        title_path = hxs.select('//title/text()').extract()
        print title_path
        # find category
        # find sub category
        url = response.url
        words = url.split('/')
        num_words = len(words)
        for i in range(3, num_words - 2):
            print "Categories: " + words[i]

        # find gender
        gender = 'M'
        if url.find('women') >= 0 or url.find('girl') >= 0:
            gender = 'F'
        print "Gender: " + gender
        
        # find name of item
        item_name_path = hxs.select('//tr/td/h1[contains (@class,"prodtitle")]/text()')
        item_name = item_name_path.extract()
        print "Name: " + str(item_name)
        
        # find price and sale price
        
        price_path = hxs.select('//td[contains (@class,"standard_nopad")]/text()')
        price_expr = '\$[\d]+\.[\d]*'
        price_regex = re.compile(price_expr)
        prices_u = price_path.re(price_regex)
        # we should have at most two unique values for prices:
        # the lower one is the sale price and higher one is the base price
        prices_float = set()
        for p in prices_u:
            p2 = p.strip('$')
            p_float = float(p2)
            prices_float.add(p_float)
        assert len(prices_float) <= 2
        price = prices_float.pop()
        sale_price = price
        if len(prices_float) == 2:
            sale_price = prices_float.pop()
            if price < sale_price:
                #swap
                other_price = sale_price
                sale_price = price
                price = other_price

        print "Price: " + str(price) + " Sale Price " + str(sale_price)

        # find colors available
        color_path = hxs.select('//select[contains (@onchange, "color")]/option/text()')
        colors = color_path.extract()
        print "Colors: " + str(colors[1:len(colors)])
        
        # find sizes available        
        size_path = hxs.select('//select[contains (@onchange, "size")]/option/text()')
        sizes = size_path.extract()
        print "Sizes: " + str(sizes[1:len(sizes)])
        
        # extract image URL
        prod_image_path = hxs.select('//div[contains (@class, "prod_main_img")]/a/img[contains (@src, "http")]/@src')
        prod_image = prod_image_path.extract()
        print "Image: " + str(prod_image)
        
        d = datetime.date.today()
        
        raise CloseSpider('Blah')
        
        return []
        
    def process_links_sub(self, links):
        # we avoid links that are un-necessary or wrong
        # for J.Crew
        return links
		
    def process_links_avoid(self, links):
        #print links
        return links

    def parse_exclude_for_testing(self, response):
        print "EXCLUDING " + str(response.url)
        return []
    
    def avoid_redirection(self, request):
        request.meta.update(dont_redirect=True)
        return request
