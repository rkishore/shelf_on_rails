from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime, urllib
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django import forms
from polls.models import Promoinfo, Items, Brands, Categories, ProductModel, CategoryModel, ColorSizeModel, WishlistM, WishlistI, UserIdMap
from django.db.models import Avg, Max, Min, Count
import match
import promotion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from chartit import DataPool, Chart
from GChartWrapper import *
from polls.models import StoreItemCombinationResults
from django.template import RequestContext
from django.forms import ModelChoiceField, ChoiceField
import copy
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str, smart_unicode

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

stores = ['Express', 'J.Crew']

def find_shelf(userid, store_name):
    itemlist = []
    final_list = WishlistI.objects.filter(user_id=userid)
    for wi in final_list:
        if wi.item.brand.name == store_name:
            catlist = CategoryModel.objects.filter(product=wi.item)
            #print catlist
            if catlist:
                itemlist.append( {"store": str(wi.item.brand), 
                                  "category": str(catlist[0].categoryName), 
                                  "name": str(wi.item.name),
                                  "price": float(wi.item.price),
                                  "sale_price": float(wi.item.saleprice),
                                  "item_idx": int(wi.item.idx)} )
            else:
                itemlist.append( {"store": str(wi.item.brand), 
                                  "category": "None", 
                                  "name": str(wi.item.name),
                                  "price": float(wi.item.price),
                                  "sale_price": float(wi.item.saleprice),
                                  "item_idx": int(wi.item.idx)} )

    return itemlist

def find_shelf_store_based_for_user(userid):
    shelf_per_store = {}
    for brand_name in stores:
        itemlist = find_shelf(userid, brand_name)
        shelf_per_store[brand_name] = itemlist
    return shelf_per_store


def apply_promo_store(userid, store_name):
    itemlist = find_shelf(userid, store_name)
    num_items = len(itemlist)
    print "Apply_promo: We have " + str(num_items) + " items in " + store_name + " shelf."
    total_combinations = 1 << (num_items)
    total_combinations -= 1
    print "Total combination: " + str(total_combinations)
    date_ = datetime.date.today()
    promo_date = Promoinfo.objects.filter(d = date_)
    if store_name == "Express":
        i = 0
    if store_name == "J.Crew":
        i = 1
    promo = promo_date.filter(store__id = i)

    # for all possible combinations
        # find the price by calling match.py
        # upper bound is total_combinations+1 because we are starting with index 1
        # and that is because we don't want to calculate discount for an empty wishlist
        # which will happen when j = 0
    
    for j in range(1, total_combinations + 1):
        wishlist = find_combination(itemlist, j)
        cached_result, digest = check_if_combination_exists(wishlist)
        if cached_result == None:
            print "No, didn't find result for list " + str(j) + " in cache, so storing it"
            orig_cost, total_cost, savings, shipping = match.match(store_name, date_, 
                                                                   copy.deepcopy(wishlist), promo)
            # store this result
            new_result = StoreItemCombinationResults(combination_id = digest,
                                                     price = orig_cost,
                                                     saleprice = total_cost,
                                                     free_shipping = shipping,)
            new_result.save()

    print "Done with apply_promo_store"
# this function is used to find all combinations
def find_combination(shelf, combination_id):
    result = []
    for i in range (0, len(shelf)):
        k = combination_id >> i
        k = k & 0x1
        #print "Combination_id " + str(hex(combination_id)) + " i " + str(hex(i+1)) + " k " + str(hex(k))
        if k == 0x1:
            result.append(shelf[i])
    return result
    

def check_if_combination_exists(list_of_items):
    m = hashlib.md5()
    for item in list_of_items:
        print item
        m.update(str(item['item_idx']))
    try:
        result = StoreItemCombinationResults.objects.get(combination_id = m.hexdigest())
        return (result, m.hexdigest())
    except ObjectDoesNotExist:
        return (None, m.hexdigest())

def apply_promo(request, d1, d2):
    if 'u' in request.GET and request.GET['u']:
        userid = urllib.unquote(request.GET['u'].decode('utf-8'))
        result_list = {}
        #for each store-shelf
        shelf_per_store = find_shelf_store_based_for_user(userid)
        for i in range(0, len(shelf_per_store)):
            # how many items in this shelf
            store_name = stores[i]
            num_items = len(shelf_per_store[store_name])
            print "Apply_promo: We have " + str(num_items) + " items in " + store_name + " shelf."
            total_combinations = 1 << (num_items)
            total_combinations -= 1
            print "Total combination: " + str(total_combinations)
            date_ = datetime.date.today()
            promo_date = Promoinfo.objects.filter(d = date_)
            promo = promo_date.filter(store__id = i)

            # for all possible combinations
                # find the price by calling match.py
                # upper bound is total_combinations+1 because we are starting with index 1
                # and that is because we don't want to calculate discount for an empty wishlist
                # which will happen when j = 0
            itemlist = []         
            for j in range(1, total_combinations + 1):
                wishlist = find_combination(shelf_per_store[store_name], j)
                cached_result, digest = check_if_combination_exists(wishlist)
                if cached_result == None:
                    print "No, didn't find result for list " + str(j) + " in cache, so storing it"
                    orig_cost, total_cost, savings, shipping = match.match(store_name, date_, 
                                                                           copy.deepcopy(wishlist), promo)
                    # store this result
                    new_result = StoreItemCombinationResults(combination_id = digest,
                                                             price = orig_cost,
                                                             saleprice = total_cost,
                                                             free_shipping = shipping,)
                    new_result.save()
                else:
                    print "Great, found the result! Using it here."
                    orig_cost = cached_result.price
                    total_cost = cached_result.saleprice
                    savings = cached_result.price - cached_result.saleprice
                    shipping = cached_result.free_shipping
                        
                print "RESULT:: " + str(j) + " " + str(store_name) + " " + str(orig_cost) + " " + str(total_cost) + " " + str(savings)
                itemlist.append( {"orig_cost": orig_cost, 
                                  "total_cost": total_cost, 
                                  "savings": savings,
                                  "shipping": shipping,})

            result_list[store_name] = itemlist  
        return list_detail.object_list(request,
                                       queryset = WishlistI.objects.none(),
                                       template_name = "apply_promo.html",
                                       extra_context = {'uid': userid,
                                                        'result_list': result_list,} )


def yourshelf_store_based(request, d1, d2):
    print 'In your_shelf_store_based'
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
            u = UserIdMap.objects.filter(user_id=userid)
            if u: #HACK!!
                print 'User ID: ', u[0].user_id, 'IP: ', u[0].ip_addr 
                final_list = WishlistI.objects.filter(user_id=u[0])
                br_list = WishlistI.objects.none()
                for wi in final_list:
                    if wi.item.brand.name == brand_name:
                        br_list = br_list | final_list.filter(item=wi.item)
                        catlist = CategoryModel.objects.filter(product=wi.item)
                    #print catlist
                        if catlist:
                            itemlist.append( {"store": smart_str(wi.item.brand), 
                                              "category": smart_str(catlist[0].categoryName), 
                                              "name": smart_str(wi.item.name),
                                              "price": float(wi.item.price),
                                              "sale_price": float(wi.item.saleprice)} )
                        else:
                            itemlist.append( {"store": smart_str(wi.item.brand), 
                                              "category": "None", 
                                              "name": smart_str(wi.item.name),
                                              "price": float(wi.item.price),
                                              "sale_price": float(wi.item.saleprice)} )
                        shelf_per_store[s] = br_list
                        num_selected_per_store[s] = len(br_list)
                selected_items[int(userid)] = itemlist
                print shelf_per_store
            else:
                return HttpResponse('Dear user: please login or create an account before accessing this page...')

            if not shelf_per_store:
                shelf_per_store[stores[0]] = br_list
                shelf_per_store[stores[1]] = br_list
                
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
        u = UserIdMap.objects.get(user_id=userid)
        final_list = WishlistI.objects.filter(user_id=u)
        br_list1 = WishlistI.objects.none()
        br_list2 = WishlistI.objects.none()
        k=0
        for wi in final_list:
            k += 1
            #print wi
            catlist = CategoryModel.objects.filter(product=wi.item)
            #print catlist
            if catlist:
                itemlist.append( {"store": smart_str(wi.item.brand), 
                                  "category": str(catlist[0].categoryName), 
                                  "name": smart_str(wi.item.name),
                                  "price": float(wi.item.price),
                                  "sale_price": float(wi.item.saleprice)} )
            else:
                itemlist.append( {"store": smart_str(wi.item.brand), 
                                  "category": "None", 
                                  "name": smart_str(wi.item.name),
                                  "price": float(wi.item.price),
                                  "sale_price": float(wi.item.saleprice)} )
            
            if wi.item.brand.name == "Express":
                tmpqset = final_list.filter(item=wi.item)
                if len(tmpqset) > 1: 
                    br_list1 = br_list1 | tmpqset[0]
                else:
                    br_list1 = br_list1 | tmpqset
            if wi.item.brand.name == "J.Crew":
                tmpqset = final_list.filter(item=wi.item)
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
            elif ('pullover' in pname):
                pname = pname.replace('pullover', 'sweater')
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
               qs_arr[i] = qs_arr[i] | WishlistI.objects.filter(user_id=u).filter(item=j)
    
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
