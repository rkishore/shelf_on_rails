from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime, urllib
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django import forms
from polls.models import Promoinfo, Items, Brands, Categories, ProductModel, CategoryModel, ColorSizeModel, WishlistM, WishlistI
from django.db.models import Avg, Max, Min, Count
import match
import promotion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from chartit import DataPool, Chart
from GChartWrapper import *

from django.template import RequestContext
from django.forms import ModelChoiceField, ChoiceField
import copy

item_list_results_hash_table = {}

selected_items_id_list = {}
selected_items = {}

NUM_COLUMNS_TABLE_TEMPLATE = 5

GENDER_CHOICES = (
                   ('M', 'MALE'),
                   ('F', 'FEMALE'),
                   ('A', 'ALL'),
                   )

### Testing ####
selected_items_id_list[112] = []
######## Visualization Sample Code #############
import gviz_api
from django.db.models import F



#### Start ShelfIt #####
dist_cat_set = set()
dist_cat_set.add('Jean')
dist_cat_set.add('Short')
dist_cat_set.add('Pant')
dist_cat_set.add('Tie')
dist_cat_set.add('Shirt')
dist_cat_set.add('Tank')
dist_cat_set.add('Skirt')
dist_cat_set.add('Dress')
dist_cat_set.add('Jacket')
dist_cat_set.add('Sweater')

items_per_cat = {}





def yourshelf_store_based(request, d1, d2):
    print "Hello"
    if 'u' in request.GET and request.GET['u']:# and (('s' in request.GET and request.GET['s']) or ('c' in request.GET and request.GET['c'])):
        
        # Get User ID
        userid = urllib.unquote(request.GET['u'].decode('utf-8'))
        
        # Brand-specific info request
        stores = ['Express', 'J.Crew']
        shelf_per_store = {}
        num_selected_per_store = {}
        for s in stores:
            brand_name = s#urllib.unquote(request.GET['s'].decode('utf-8'))
            print s
            selected_items[int(userid)] = []
            itemlist = []
            final_list = WishlistI.objects.filter(user_id=userid)
            br_list = WishlistI.objects.none()
            for wi in final_list:
                if wi.item.brand.name == brand_name:
                    br_list = br_list | WishlistI.objects.filter(item=wi.item)
                    catlist = CategoryModel.objects.filter(product=wi.item)
                    #print catlist
                    if catlist:
                        itemlist.append( {"store": str(wi.item.brand), 
                                          "category": str(catlist[0].categoryName), 
                                          "name": str(wi.item.name),
                                          "price": float(wi.item.price),
                                          "sale_price": float(wi.item.saleprice)} )
                    else:
                        itemlist.append( {"store": str(wi.item.brand), 
                                          "category": "None", 
                                          "name": str(wi.item.name),
                                          "price": float(wi.item.price),
                                          "sale_price": float(wi.item.saleprice)} )
                shelf_per_store[s] = br_list
                num_selected_per_store[s] = len(br_list)
            selected_items[int(userid)] = itemlist
            print shelf_per_store
        return list_detail.object_list(request,
                                       queryset = shelf_per_store[stores[0]],
                                       template_name = "view_shelf.html",
                                       extra_context = {'selected_items' : True,
                                                        'store_based': True,
                                                        'category_based': False, 
                                                        'num_selected' : num_selected_per_store,#len(shelf_per_store), 
                                                        'uid': userid,
                                                        'shelfs': shelf_per_store,} )
        
                  
    else:
        return HttpResponse('Dear user: please login or create an account before accessing this page...')

def yourshelf_category_based(request, d1, d2):

    if 'u' in request.GET and request.GET['u']:
        # Get User ID
        userid = urllib.unquote(request.GET['u'].decode('utf-8'))
        
        # Get Info brand-wise
        selected_items[int(userid)] = []
        itemlist = []
        final_list = WishlistI.objects.filter(user_id=userid)
        br_list1 = WishlistI.objects.none()
        br_list2 = WishlistI.objects.none()
        k=0
        for wi in final_list:
            k += 1
            #print wi
            catlist = CategoryModel.objects.filter(product=wi.item)
            #print catlist
            if catlist:
                itemlist.append( {"store": str(wi.item.brand), 
                                  "category": str(catlist[0].categoryName), 
                                  "name": str(wi.item.name),
                                  "price": float(wi.item.price),
                                  "sale_price": float(wi.item.saleprice)} )
            else:
                itemlist.append( {"store": str(wi.item.brand), 
                                  "category": "None", 
                                  "name": str(wi.item.name),
                                  "price": float(wi.item.price),
                                  "sale_price": float(wi.item.saleprice)} )
            
            if wi.item.brand.name == "Express":
                tmpqset = WishlistI.objects.filter(item=wi.item)
                if len(tmpqset) > 1: 
                    br_list1 = br_list1 | tmpqset[0]
                else:
                    br_list1 = br_list1 | tmpqset
            if wi.item.brand.name == "J.Crew":
                tmpqset = WishlistI.objects.filter(item=wi.item)
                if len(tmpqset) > 1: 
                    br_list2 = br_list2 | tmpqset[0]
                else:
                    br_list2 = br_list2 | tmpqset
                    
        selected_items[int(userid)] = itemlist
        
        # Get Info category-wise
        catlist = set()
        itemidx = {}
        k = 0
        for wi in final_list:
            pname = wi.item.name.lower()
            if ('cardigan' in pname):
                pname = pname.replace('cardigan', 'sweater')
            elif ('hoodie' in pname):
                pname = pname.replace('hoodie', 'sweater')
            elif ('henley' in pname):
                pname = pname.replace('henley', 't-shirt')
            elif (not 'dress' in pname) and (not 'skirt' in pname) and ('tee' in pname):
                pname = pname.replace('tee', 't-shirt')
            elif 'cami' in pname:
                pname = pname.replace('cami', 'tank')
            elif 'blazer' in pname:
                pname = pname.replace('blazer', 'jacket')
            
            k=0
            for i in dist_cat_set:
                if i.lower() in pname:
                    if i not in catlist:
                        catlist.add(i)
                    tmparr = []
                    try:
                        for j in itemidx[i]:
                            tmparr.append(j)
                    except KeyError:
                        pass
                    tmparr.append(wi.item)
                    itemidx[i] = tmparr
                    break
                else:
                    k += 1
                    if (k == len(dist_cat_set)):
                        print "LOST:", pname
        
        #print k, len(catlist), len(final_list), catlist, itemidx
        
        qs_arr = {}
        for i in catlist:
            qs_arr[i] = WishlistI.objects.none()
            for j in itemidx[i]:
               qs_arr[i] = qs_arr[i] | WishlistI.objects.filter(item=j)
    
        #print qs_arr
        items_per_cat[userid] = qs_arr
        #print cat_name, qs_arr
        print qs_arr
        return list_detail.object_list(request,
                                       queryset = WishlistI.objects.none(),
                                       template_name = "view_shelf.html",
                                       extra_context = {'selected_items' : True,
                                                        'store_based': False,
                                                        'category_based': True, 
                                                        'uid': userid,
                                                        'shelfs': qs_arr,} )
    else:
        return HttpResponse('Dear user: please login or create an account before accessing this page...')
