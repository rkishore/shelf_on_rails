import re
import copy
import datetime
import os, errno
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from crawler.items import Category, ProductItem, ColorSizeItem, CategoryItem
from tutorial.polls.models import Brands, ProductModel
from BeautifulSoup import BeautifulSoup

dnow = datetime.datetime.now()
df = dnow.isoformat()
dirpath = "/home/kishore/ParsingData/" + df + "/" 
brandname = "Express"

def mkdir_p(fpath):
    print "Creating directory: ", fpath
    try:
        os.makedirs(fpath)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def init_model_values():

    item = ProductItem()
    category = CategoryItem() 
    colorsize = ColorSizeItem()
    
    b = Brands.objects.all()
    item['brand'] = b[0]
    item['idx'] = -11111
    item['name'] = "None"
    item['prod_url'] = "None"
    item['price'] = -111.00
    item['saleprice'] = -111.00
    item['promo_text'] = "None"
    item['err_text'] = "None"
    item['gender'] = "None"
    item['img_url'] = "None"
   
    cat_arr = []
    cs_arr = []
    
    return item, cat_arr, cs_arr

def fill_item_info1(s1, item):
    item['name'] = s1.h1.text
    for i in s1.findAll('li'):
       try:
          if i['class'] == "cat-pro-price":
             j = i.findAll('span')
             if j:
                try:
                   if j['class'] == "cat-glo-tex-oldP":
                      item['price'] = j.text.split('$')[1]
                   elif j['class'] == "cat-glo-tex-saleP":
                      item['saleprice'] = j.text.split('$')[1]
                except:
                   pass
             else:
                k = i.findAll('strong')
                for l in k:
                   if l.text:
                      item['price'] = l.text.split('$')[1]
                      item['saleprice'] = l.text.split('$')[1]
       except KeyError:
          #print "KeyError", i
          pass
    return

def fill_item_info2(s1, item):
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
    return

def fill_itemcat_info1(soup, item, category_arr):
    l_cat_id = -1
    l_subcat_id = -1
    l_cat_name = ""
    l_subcat_name = ""
    s4= soup.findAll('input')
    if s4:
        for i in s4:
            try:
                 #print i['name']
                 if (i['name'] == 'productId'):
                     item['idx'] = i['value']
                 if (i['name'] == 'parentCategoryId'):
                     if (i['value'] == "1"):
                         item['gender'] = "M"
                     elif (i['value'] == "2"):
                         item['gender'] = "F"
                 if (i['name'] == 'categoryId'):
                     l_cat_id = i['value']
                     #category['categoryId'] = i['value']
                 if (i['name'] == 'subCategoryId'):
                     l_subcat_id = i['value']
                     #category['subCategoryId'] = i['value']
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
                    l_cat_name = i.text
                    #category['categoryName'] = i.text
                if i['id'] == 'breadURL_Thumb':
                    l_subcat_name = i.text
                    #  category['subCategoryName'] = i.text
            except KeyError:
                pass
    
    # Single category?
    if (l_cat_id == l_subcat_id):
        cat1 = CategoryItem()
        cat1['categoryId'] = l_cat_id
        cat1['categoryName'] = l_subcat_name
        category_arr.append(cat1)
    else:
        # Multiple categories
        for l in range(0,2):
            cat1 = CategoryItem()
            if (l==0):
                cat1['categoryId'] = l_cat_id
                cat1['categoryName'] = l_cat_name
            else:
                cat1['categoryId'] = l_subcat_id
                cat1['categoryName'] = l_subcat_name
            category_arr.append(cat1)
            
    
    if not len(category_arr):
        cat1 = CategoryItem()
        cat1['categoryId'] = -11
        cat1['categoryName'] = "None"
        category_arr.append(cat1)  
    
    # Get image url
    s7 = soup.find('link', {'rel' : 'image_src'})
    if s7:
        item['img_url'] = s7['href'].split('?')[0]
      
    return
    
       
def fill_itemcat_model(soup, item, category_arr, response):
    item['prod_url'] = response.url
    s1 = soup.find('div', {'id' : 'cat-pro-con-detail'})
    if s1:
        fill_item_info1(s1, item)
        fill_item_info2(s1, item)
    fill_itemcat_info1(soup, item, category_arr) 
    return

def fill_colorsize_model(response, colorsize_arr):
    
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
    
    for i in l_size:
        for j in l_size[i]:
            cs = ColorSizeItem()
            cs['color'] = i
            if not j == "No Size":
                cs['size'] = j
            else:
                cs['size'] = "None"  
            colorsize_arr.append(cs)
    
    if not len(colorsize_arr):
        cs = ColorSizeItem()
        cs['color'] = "None"
        cs['size'] = "None"
        colorsize_arr.append(cs)
    
    return  
     

def save_to_file(soup, item):
    fname = dirpath + brandname + "-" + item['idx'] + ".html"
    #print "FILE DEBUG:", fname
    f = open(fname, 'w')
    f.write(soup.prettify())
    f.close()
    return

def save_to_db(item, category_arr, colorsize_arr):
    cur_it = item.save()
    for cur_cat in category_arr:
        cur_cat['product'] = ProductModel.objects.get(pk=cur_it.id)
        cur_cat.save()
        
    for cur_cs in colorsize_arr:
        cur_cs['product'] = ProductModel.objects.get(pk=cur_it.id)
        cur_cs.save()
    
class ExpressSpider(BaseSpider):
   name = "express"
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
      for i in range(0, 2):
         for j in s1[i].ul.findAll('li'):
            ind_cat = Category()
            try: 
               ind_cat['name'] = j.a.text
               ind_cat['url'] = j.a['href']         
            except AttributeError:
               print "AttributeError", j
               continue
            else:
               if not (ind_cat['name'] == "Must-Have Looks" or
                       ind_cat['name'] == "Gift Cards"):
                #if (ind_cat['name'] == "Women's Clothing Sale"):
                #if (ind_cat['name'] == "Fashion Accessories"): 
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
      item, category_arr, colorsize_arr = init_model_values()
      fill_itemcat_model(soup, item, category_arr, response)
      fill_colorsize_model(soup, colorsize_arr)
      save_to_file(soup, item)
      save_to_db(item, category_arr, colorsize_arr)
       
      return item   

