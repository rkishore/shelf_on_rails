import datetime, urllib, copy, hashlib
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic import list_detail
from django.db.models import Avg, Max, Min, Count
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str, smart_unicode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect

from debra.models import StoreItemCombinationResults
from debra.models import Promoinfo, Items, Brands, Categories, ProductModel, CategoryModel, ColorSizeModel, WishlistI, UserIdMap
from angel import match
from masuka import categorize, find_price_jcrew

#import promotion

PROD_MODEL_BASED = 0
SHOPSTYLE_BASED = 1
NAME_BASED = 2

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

selected_items_id_list = {}
selected_items = {}
selected_items_id_list[112] = []
stores = ['Express', 'J.Crew']

def insert_product_in_wishlist_new(userid, size_, color_, quantity_, imgurl_, matched_prod_obj):
    
    # Get UserId object. This should not fail as the userid is created on the home page
    u = UserIdMap.objects.get(user_id=userid)
    
    # Check if item already in database
    w = WishlistI.objects.filter(user_id=u).filter(item=matched_prod_obj)
    if not w:
        w = WishlistI()
        w.user_id = u
        w.size = size_
        w.color = color_
        w.quantity = quantity_
        w.img_url = imgurl_
        w.item = matched_prod_obj
        w.save()
        resp = "Added Item to Wishlist!"
    else:
        resp = "Item already in Wishlist!"
    return w, resp

def render_single_item(request, userid, prod, resp):
    wishlist_id_ = 112
    selected_items[int(wishlist_id_)] = []
    itemlist = []
    uid_obj = UserIdMap.objects.get(user_id=userid)
    final_list = WishlistI.objects.filter(item=prod).filter(user_id=uid_obj)
    for wi in final_list:
        catlist = CategoryModel.objects.filter(product=wi)
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
    
    selected_items[int(wishlist_id_)] = itemlist
    return list_detail.object_list(request,
                                   queryset = final_list,
                                   template_name = "item_table.html",
                                   extra_context = {'curresp' : resp, 
                                                    'num_selected' : len(final_list), 
                                                    'uid': userid} )

def shelfit(request, d1, d2):
     
    print "Inside shelfit"
    if 'u' in request.GET and request.GET['u'] and\
        't' in request.GET and request.GET['t'] and\
        's' in request.GET and request.GET['s'] and\
        'c' in request.GET and request.GET['c'] and\
        'q' in request.GET and request.GET['q'] and\
        'imgurl' in request.GET and request.GET['imgurl']:
        
        # Get User ID
        userid = urllib.unquote(request.GET['t'].decode('utf-8'))
        
        # Get product URL
        prod_url = urllib.unquote(request.GET['u'].decode('utf-8')) 
        
        # Get item ID and brand name
        spl1 = prod_url.split("/")
        brand_name_arr = spl1[2].split(".")
        if not len(brand_name_arr) > 1:
            return render_to_response('err_display.html', {'errmsg' : 1})
        else:
            brand_name = brand_name_arr[1]
        
            prod_id = -111
            prod_info = []
            for i in range(3, len(spl1)):
                if (brand_name == "express"): 
                    prod_info = spl1[i].split("-")
                elif (brand_name == "jcrew"):
                    prod_info = spl1[i].split("~")
                for i in prod_info:
                    try:
                        prod_id = int(i)
                    except ValueError:
                        pass
                    else:
                        break
                if (prod_id > 0):
                    break
            
            if (((brand_name == 'express') or (brand_name == 'jcrew')) and 
                (prod_id > 0)):
                
                if brand_name == 'express': 
                    br_obj = Brands.objects.get(name=stores[0])
                elif brand_name == 'jcrew':
                    br_obj = Brands.objects.get(name=stores[1]) 
                
                # Find product in database
                date_ = datetime.date(2000, 1, 11)
                prod_arr = ProductModel.objects.filter(brand=br_obj).filter(idx=prod_id).filter(insert_date=date_)
                
                if prod_arr:
                    print userid, prod_arr[0].idx
                
                    # Get size, color, quantity, and img_url
                    size_ = urllib.unquote(request.GET['s'].decode('utf-8'))
                    color_ = urllib.unquote(request.GET['c'].decode('utf-8'))
                    quantity_ = urllib.unquote(request.GET['q'].decode('utf-8'))
                    
                    if (brand_name == 'express'):
                        imgurl_ = urllib.unquote(request.GET['imgurl'].decode('utf-8')).split("?")[0]
                    elif (brand_name == 'jcrew'):
                        imgurl_ = urllib.unquote(request.GET['imgurl'].decode('utf-8'))
                        
                    print imgurl_
                    
                    #print size_, color_, quantity_, imgurl_
                    
                    # Add product to wishlist
                    w, resp = insert_product_in_wishlist_new(userid, size_, color_, quantity_, imgurl_, prod_arr[0])
                    
                    # From show_selected_items_new
                    return render_single_item(request, userid, prod_arr[0], resp)
                
                else:
                    return render_to_response('err_display.html', {'errmsg' : 2}) 
            else:
                if not ((brand_name == "express") or (brand_name == "jcrew")):
                    return render_to_response('err_display.html', {'errmsg' : 1})
                else:
                    return render_to_response('err_display.html', {'errmsg' : 3})
    else:
        return render_to_response('err_display.html', {'errmsg' : 3})

def remove_item(request, d1, d2):
    print "Inside remove_item"
    if 'u' in request.GET and request.GET['u'] and 'i' in request.GET and request.GET['i']:
        userid_ = request.GET['u'].decode('utf-8')
        itemid_ = request.GET['i'].decode('utf-8')
        print userid_, itemid_
        u = UserIdMap.objects.all()
        for i in u:
            if i.user_id == int(userid_):
                print "Found user_id", userid_
                w = WishlistI.objects.filter(user_id=i)
                for j in w:
                    if j.id == int(itemid_):
                        print "Found itemid", itemid_
                        j.delete()
                        #return render_single_item(request, userid_, prod_arr[0], 'Deleted Item')
                        #return render_store_shelf(request, userid_)
                        return redirect('/viewyourshelf/?u='+userid_)
                    else:
                        print j.id, itemid_
                        #return render_to_response('err_display.html', {'errmsg' : 7})
            else:
                print userid_, i.user_id
    else:
        return render_to_response('err_display.html', {'errmsg' : 3})
    

def render_store_shelf(request, userid):
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
            print "FINAL_LIST: " + str(final_list)
            br_list = WishlistI.objects.none()
            for wi in final_list:
                if wi.item.brand.name == brand_name:
                    br_list = br_list | final_list.filter(item=wi.item)
                    catlist = CategoryModel.objects.filter(product=wi.item)
                    print "IMG_URL: " + str(wi.item.img_url)
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
            print "SHELF_PER_STORE: " + str(shelf_per_store)
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

def find_shelf_store_based_for_user(userid):
    shelf_per_store = {}
    for brand_name in stores:
        selected_items[int(userid)] = []
        itemlist = []
        u = UserIdMap.objects.get(user_id=userid)
        final_list = WishlistI.objects.filter(user_id=u)
        for wi in final_list:
            print wi.item.prod_url, wi.item.promo_text
            if wi.item.brand.name == brand_name:
                catlist = CategoryModel.objects.filter(product=wi.item)
                #print catlist
                if catlist:
                    cat_arr = []
                    for c in catlist:
                        cat_arr.append(c.categoryName)
            
                    itemlist.append( {"store": smart_str(wi.item.brand), 
                                      "category": "; ".join(cat_arr), 
                                      "name": smart_str(wi.item.name),
                                      "price": float(wi.item.price),
                                      "sale_price": float(wi.item.saleprice),
                                      "item_idx": int(wi.item.idx)} )
                else:
                    itemlist.append( {"store": smart_str(wi.item.brand), 
                                      "category": "None", 
                                      "name": smart_str(wi.item.name),
                                      "price": float(wi.item.price),
                                      "sale_price": float(wi.item.saleprice),
                                      "item_idx": int(wi.item.idx)} )
        shelf_per_store[brand_name] = itemlist
    return shelf_per_store

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
    

def check_if_combination_exists(list_of_items, date_):
    m = hashlib.md5()
    for item in list_of_items:
        print item
        m.update(str(item.item.idx))
    m.update(str(date_))
    try:
        result = StoreItemCombinationResults.objects.get(combination_id = m.hexdigest())
        return (result, m.hexdigest())
    except ObjectDoesNotExist:
        return (None, m.hexdigest())

def yourshelf_store_based(request, d1, d2):
    
    print 'In your_shelf_store_based'
    
    if 'u' in request.GET and request.GET['u']:# and (('s' in request.GET and request.GET['s']) or ('c' in request.GET and request.GET['c'])):    
        # Get User ID
        userid = urllib.unquote(request.GET['u'].decode('utf-8'))
        return render_store_shelf(request, userid)
    else:
        return render_to_response('err_display.html', {'errmsg': 5})

def yourshelf_category_based(request, d1, d2):

    if 'u' in request.GET and request.GET['u']:
        # Get User ID
        userid = urllib.unquote(request.GET['u'].decode('utf-8'))
        
        # Get Info brand-wise
        selected_items[int(userid)] = []
        itemlist = []
        u = UserIdMap.objects.get(user_id=userid)
        final_list = WishlistI.objects.filter(user_id=u)
        
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
        return render_to_response('err_display.html', {'errmsg' : 5})

def apply_promo(request, d1, d2):
    if 'u' in request.GET and request.GET['u']:
        userid = urllib.unquote(request.GET['u'].decode('utf-8'))
        u = UserIdMap.objects.filter(user_id=userid)
        user_wish_list = WishlistI.objects.filter(user_id=u[0])
        print user_wish_list
        store_list_express = []
        store_list_jcrew = []
        result_list = {}
        date_ = datetime.date.today()

        for wi in user_wish_list:
            print "WI.ITEM: " + str(wi.item)
            if wi.item.brand.name == "Express":
                store_list_express.append(wi)
            if wi.item.brand.name == "J.Crew":
                store_list_jcrew.append(wi)
        
        if len(store_list_express) > 0:
            cached_result, digest = check_if_combination_exists(store_list_express, date_)
            if cached_result == None:
                result = find_price_jcrew.calculate_price_for_express(store_list_express)
                new_result = StoreItemCombinationResults(combination_id = digest,
                                                         price = result[0]['orig_cost'],
                                                         saleprice = result[0]['total_cost'],
                                                         free_shipping = result[0]['shipping'],)
                new_result.save()
                result_list['Express'] = result
            else:
                result = []
                result.append({"orig_cost": cached_result.price,
                               "total_cost": cached_result.saleprice,
                               "savings": cached_result.price - cached_result.saleprice,
                               "shipping": cached_result.free_shipping, })
                result_list['Express'] = result
        if len(store_list_jcrew) > 0:
            cached_result, digest = check_if_combination_exists(store_list_jcrew, date_)
            if cached_result == None:
                result = find_price_jcrew.calculate_price_for_jcrew(store_list_jcrew)
                new_result = StoreItemCombinationResults(combination_id = digest,
                                                         price = result[0]['orig_cost'],
                                                         saleprice = result[0]['total_cost'],
                                                         free_shipping = result[0]['shipping'],)
                new_result.save()
                result_list['J.Crew'] = result
            else:
                result = []
                result.append({"orig_cost": cached_result.price,
                               "total_cost": cached_result.saleprice,
                               "savings": cached_result.price - cached_result.saleprice,
                               "shipping": cached_result.free_shipping, })
                result_list['J.Crew'] = result
        #result_list = find_price_jcrew.calculate_price_for_wishlist(userid)
        
        ''' OLDER CODE BASE '''
        if 0:
            result_list = {}
            #for each store-shelf
            shelf_per_store = find_shelf_store_based_for_user(userid)
            print shelf_per_store
            cat_scheme = PROD_MODEL_BASED
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
                promo = promo_date.filter(store__id = i + 1)
                print promo
                print date_
                # for all possible combinations
                    # find the price by calling match.py
                    # upper bound is total_combinations+1 because we are starting with index 1
                    # and that is because we don't want to calculate discount for an empty wishlist
                    # which will happen when j = 0
                itemlist = []
                for j in range(1, total_combinations + 1):
                    wishlist = find_combination(shelf_per_store[store_name], j)
                    wishlist_categories = categorize.find_wishlist_cat(wishlist, PROD_MODEL_BASED)
                    print wishlist, wishlist_categories
                    #return render_to_response('err_display.html', {'errmsg' : 4})
                    cached_result, digest = check_if_combination_exists(wishlist)
                    if cached_result == None:
                        print "No, didn't find result for list " + str(j) + " in cache, so storing it"
                        orig_cost, total_cost, savings, shipping = match.match(store_name, copy.deepcopy(wishlist), wishlist_categories, promo)
                        # store this result
                        new_result = StoreItemCombinationResults(combination_id = digest,
                                                                 price = orig_cost,
                                                                 saleprice = total_cost,
                                                                 free_shipping = shipping,)
                        #new_result.save()
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
