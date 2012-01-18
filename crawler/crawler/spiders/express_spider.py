import re
import copy
import datetime
import os, errno
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from stutorial.items import Category, Product
from BeautifulSoup import BeautifulSoup

dnow = datetime.datetime.now()
df = dnow.isoformat()
dirpath = "/home/kishore/ParsingData/" + df + "/" 
brandname = "express"

def mkdir_p(fpath):
    print "Creating directory: ", fpath
    try:
        os.makedirs(fpath)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

class Express2Spider(BaseSpider):
   name = "express2"
   allowed_domains = ["express.com"]
   start_urls = [
      "http://www.express.com/custserv/custserv.jsp?pageName=Sitemap",
      ]

   def parse(self, response):      
      myMassage = [(re.compile('([^-])-----!>'), lambda match: '-->' + match.group(1))]
      myNewMassage = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
      myNewMassage.extend(myMassage)
      soup = BeautifulSoup(response.body_as_unicode(), markupMassage=myNewMassage)
     
      mkdir_p(dirpath)
      
      s1 = soup.findAll('div', {'class' : 'cus-sit-column'})
      for i in range(1, 2):
         for j in s1[i].ul.findAll('li'):
            ind_cat = Category()
            try: 
               ind_cat['name'] = j.a.text
               ind_cat['url'] = j.a['href']         
            except AttributeError:
               print "AttributeError", j
               continue
            else:
               #if not (ind_cat['name'] == "Must-Have Looks" or
               #        ind_cat['name'] == "Gift Cards"):
                #if (ind_cat['name'] == "Women's Clothing Sale"):
                if (ind_cat['name'] == "Fashion Accessories"): 
                  #    ind_cat['name'] == "Men's Casual Tees & Hoodies" or 
                  #    ind_cat['name'] == "1MX Shirts"):
                  yield Request(ind_cat['url'], self.parse_viewall)
                  
            #yield ind_cat

      return
   
   def parse_viewall(self, response):

      soup = BeautifulSoup(response.body_as_unicode())
      base_url = get_base_url(response)
      
      # Click on view-all button
      s1 = soup.find('td', {'class' : 'cat-thu-but-view-all'})
      if s1:
         str_url = str(s1.a['href'])
         if (str_url.startswith("http://")):
            url_follow = s1.a['href']
         else: 
            url_follow = urljoin_rfc(base_url, s1.a['href'])
            yield Request(url_follow, self.parse_items)

      else:
         
         prod_info = soup.findAll('li', {'class' : 'cat-cat-prod-name'})                  
         if not len(prod_info):
            prod_info = soup.findAll('li', {'class' : 'cat-thu-name'})         
            
         for i in prod_info:
            try:
               str_url = str(i.a['href'])
               if (str_url.startswith("http://")):
                  url_follow = i.a['href']
               else: 
                  url_follow = urljoin_rfc(base_url, i.a['href'])
               yield Request(url_follow, self.get_prodinfo)
               #yield self.get_prodinfo(url_follow)
            except KeyError:
               pass
            
      return
   
   def parse_items(self, response):

      soup = BeautifulSoup(response.body_as_unicode())
      base_url = get_base_url(response)
      prod_info = soup.findAll('li', {'class' : 'cat-cat-prod-name'})                  
      if not len(prod_info):
         prod_info = soup.findAll('li', {'class' : 'cat-thu-name'})         
         
      for i in prod_info:
         try:
            str_url = str(i.a['href'])
            if (str_url.startswith("http://")):
               url_follow = i.a['href']
            else: 
               url_follow = urljoin_rfc(base_url, i.a['href'])
            yield Request(url_follow, self.get_prodinfo)
            #yield self.get_prodinfo(url_follow)
         except KeyError:
            pass
               
      s3 = soup.find('td', {'class' : 'cat-glo-page-action'})
      if (s3 and s3.a.text == "next"):
         str_url = str(s3.a['href'])
         if (str_url.startswith("http://")):
            url_follow = s3.a['href']
         else: 
            url_follow = urljoin_rfc(base_url, s3.a['href'])
            yield Request(url_follow, self.parse_items)
            
      return

   def get_prodinfo(self, response):
       
      soup = BeautifulSoup(response.body_as_unicode())
      item = Product()
      
      item['url'] = response.url
      
      #print soup.prettify()
      
      s1 = soup.find('div', {'id' : 'cat-pro-con-detail'})
      if s1:
         item['name'] = s1.h1.text

         for i in s1.findAll('li'):
            try:
               if i['class'] == "cat-pro-price":
                  j = i.findAll('span')
                  if j:
                     try:
                        if j['class'] == "cat-glo-tex-oldP":
                           item['price'] = j.text
                        elif j['class'] == "cat-glo-tex-saleP":
                           item['saleprice'] = j.text
                     except:
                        pass
                  else:
                     k = i.findAll('strong')
                     for l in k:
                        if l.text:
                           item['price'] = l.text
                           item['saleprice'] = l.text

            except KeyError:
               #print "KeyError", i
               pass
           
         s2 = s1.find('span', {'class' : 'cat-pro-promo-text'})
         if s2:
            try:
                item['promo_text'] = s2.font.text
            except AttributeError:
                item['promo_text'] = s2.text
    
         s3 = s1.find('span', {'class' : 'glo-tex-error'})
         if s3:
            try:
                item['err_text'] = s3.font.text
            except AttributeError:
                item['err_text'] = s3.text

      s4= soup.findAll('input')
      if s4:
          item['idx'] = None
          item['gender'] = None
          item['categoryId'] = None
          item['subCategoryId'] = None

          for i in s4:
              try:
                  #print i['name']
                  if (i['name'] == 'productId'):
                      item['idx'] = i['value']
                      fname = dirpath + brandname + "-" + item['idx'] + ".html"
                      #print "FILE DEBUG:", fname
                      f = open(fname, 'w')
                      f.write(soup.prettify())
                      f.close()
                      
                  if (i['name'] == 'parentCategoryId'):
                      if (i['value'] == "1"):
                          item['gender'] = "M"
                      elif (i['value'] == "2"):
                          item['gender'] = "F"
                  
                  if (i['name'] == 'categoryId'):
                      item['categoryId'] = i['value']

                  if (i['name'] == 'subCategoryId'):
                      item['subCategoryId'] = i['value']
 
              except KeyError:
                  pass
      else:
          print "input not found"
      
      s5 = soup.find('div', {'id' : 'glo-cat-breadcrumb-area'})
      if s5:
          s6 = s5.findAll('a')
          for i in s6:
              try:
                  if i['id'] == 'breadURL_Cat':
                    item['categoryName'] = i.text
                  
                  if i['id'] == 'breadURL_Thumb':
                    item['subCategoryName'] = i.text
              except KeyError:
                  pass

      s7 = soup.find('link', {'rel' : 'image_src'})
      if s7:
          item['img_url'] = s7['href'].split('?')[0]
      
      # Find Color and corresponding sizes
      str_list = re.findall('colorToSize[\w\d\[\]\\\',=\s]+;', str(response.body))
      l_color = []
      l_size = {}
      for i in str_list:
         spl1 = i.split("=")[0].split("[")[1].split("]")
      
         # Get color
         lc = unicode(spl1[0].replace("'", "").strip())
         l_color.append(lc)
         
         # Get size
         spl2 = i.split("=")[1].split("[")[1].split("];")[0].split(",")
         adj_spl2 = []
         for j in spl2:
             adj_spl2.append(unicode(j.replace("'", "").strip()))
         l_size[lc] = adj_spl2
    
      item['colors'] = l_color #'+'.join(l_color)
      item['sizes'] = l_size
      
      return item   

