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
    store_name = "j.crew"
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
            
    def _store_in_file(self, response, item_id, store_name, date):
        fname = "/tmp/" + item_id + "-" + store_name + "-" + str(date) + ".html"
        FILE = open(fname, 'w')
        FILE.write(str(response.body))
        FILE.close()
            
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
        item_expr = '[\$]*[\d,]+[\.\d]*'
        item_regex = re.compile(item_expr)
        items_u = price_path.re(item_regex)
        print items_u
        # now get item_id and price from this 
        # the price is the base price without sale
        item_id = []
        price = []
        for item in items_u:
            if self._contains(item, '$'):
                item2 = item.strip('$').replace(',', '')
                price.append(item2)
            else:
                item_id.append(item)
            
        # this array contains the current price of the item
        # and associated item_id
        # using both these arrays, we can figure out if an item is on sale
        item_options_path = hxs.select('//input[contains (@onclick, "send")]')
        item_options = item_options_path.extract()
        selection_exp = '[\d]+[,\.\d]*'
        selection_regex = re.compile(selection_exp)
        selections_u = item_options_path.re(selection_regex)
        num_selections = len(selections_u)/4
        print "Selections: " + str(selections_u) + " size " + str(len(selections_u)/4)
        
        item_id_selection = []
        sale_price = []

        # first element = item_id, second_element = price        
        for j in range(0, num_selections):
            slot = j*4
            print "Index: " + str(j) + " slot " + str(slot) + " len(selections_u) " + str(len(selections_u))
            item_id_selection.append(selections_u[slot])
            sale_price.append(selections_u[slot +1])
        
        for j in range(0, len(sale_price)):
            print "Price: " + str(price[j]) + " Sale Price " + str(sale_price[j]) + " Item " + str(item_id[j])

        # find colors available
        color_path = hxs.select('//select[contains (@onchange, "color")]/option/text()')
        colors = color_path.extract()
        print "Colors: " + str(colors[1:len(colors)])
        colors_combined = self._combine(colors[1:len(colors)], '[', ']')
        print colors_combined
        # find sizes available        
        size_path = hxs.select('//select[contains (@onchange, "size")]/option/text()')
        sizes = size_path.extract()
        print "Sizes: " + str(sizes[1:len(sizes)])
        sizes_combined = self._combine(sizes[1:len(sizes)], '[', ']')
        print sizes_combined
        
        # extract image URL
        prod_image_path = hxs.select('//div[contains (@class, "prod_main_img")]/a/img[contains (@src, "http")]/@src')
        prod_image = prod_image_path.extract()
        print "Image: " + str(prod_image)
        
        date = datetime.date.today()
        self._store_in_file(response, item_id[0], self.store_name, date)
        #raise CloseSpider('Blah')
        
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
