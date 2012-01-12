# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django import forms
from polls.models import Promoinfo, Items, Brands, Categories
from django.db.models import Avg, Max, Min, Count
import match
import promotion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from chartit import DataPool, Chart
from GChartWrapper import *
import logging
from django.template import RequestContext
from django.forms import ModelChoiceField, ChoiceField
import copy
from django.db.models import F


#logging.basicConfig(format='%(message)s', level=logging.INFO)
'''We simulate from 0-2 items selected from each category to create
    artificial wish lists. And then we calculate the prices for these
    wishlists to obtain insights. NUM_ITEMS_SIMULATED is the number of
    choices we have for each category.
'''
NUM_ITEMS_SIMULATED = 2

stores = ("Express", "J.Crew", "Banana Republic")
cats = ("shirts", "jeans", "skirts", "sweaters")    


''' Currently we have this as an in-memory array'''
price_of_wishlist = []


'''Our in-memory cache of db-query results. Later we 
want to use memchached'''
db_querysets = {}

MINIMUM = 0
MAXIMUM = 1
MEDIAN = 2

sort_order = 0
class DemoWishlist(forms.Form):
    GENDER_CHOICES = (
                   (0, 'MALE'),
                   (1, 'FEMALE'),
                   (2, 'ALL'),
                   )
    NUM_CHOICES = (
                   (0, 0),
                   (1, 1),
                   (2, 2),
                   (3, 3)
                   )
   
    shirts = forms.ChoiceField(choices = NUM_CHOICES, initial=1)
    jeans = forms.ChoiceField(choices = NUM_CHOICES, initial=1)
    skirts = forms.ChoiceField(choices = NUM_CHOICES, initial=1)
    sweaters = forms.ChoiceField(choices = NUM_CHOICES, initial=1)
    gender = forms.ChoiceField(choices = GENDER_CHOICES, initial=1)
    #size = forms.IntegerField()
    #color = forms.IntegerField()



def start(request):
    '''
    provide an initial wish list consisting of k categories and an item
    is selected from each category to create a wish list
    The item from each category is the cheapest item in that category
    from a given store.
    Now, each wishlist is then applied promotions to find the best price.
    This is final price presented to the user. 
    We also want to maintain the list of items from each category that satisfy
    the price so that the user can view what items satisfy his constraint.
    '''
    result = ""
    global price_of_wishlist
    price_of_wishlist = []

    if request.method == 'POST': # If the form has been submitted...
        form = DemoWishlist(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            demand = fill_demand(form)
            date = datetime.date.today()
            val_str, val_cost, val_savings, val_free_shipping = calculate_price_for_demand(demand, date)
            result += val_str    
    else:
        form = DemoWishlist()
        result += calculate_price_for_simulated_demands(MEDIAN)
    logging.debug(price_of_wishlist)    
    return render_to_response('mock_wishlist.html', 
                              {'form': form, 
                               #'results': result,
                               'price_wishlist': price_of_wishlist,}, 
                              context_instance=RequestContext(request))

def calculate_price_for_simulated_demands(sort_order):
    num = 0
    date = datetime.date.today()
    result = ""
    t1 = datetime.datetime.now()
    for i in range(0, NUM_ITEMS_SIMULATED):
        for j in range(0,NUM_ITEMS_SIMULATED):
            for k in range(0,NUM_ITEMS_SIMULATED):
                for l in range(0,NUM_ITEMS_SIMULATED):
                        demand = {}
                        demand[cats[0]] = i
                        demand[cats[1]] = j
                        demand[cats[2]] = k
                        demand[cats[3]] = l
                        demand['gender'] = 0
                        demand['sort_order'] = sort_order
                        logging.debug(demand)
                        num += 1
                        result += "<br>==================================<br>"
                        result += "<br>=== DEMAND: " + str(demand) + "<br>"
                        val_str, val_cost, val_savings, val_free_shipping = calculate_price_for_demand(demand, date)
                        logging.critical("Done with demand " + str(num))
                        result += val_str
    t2 = datetime.datetime.now()
    t3 = t2 - t1
    logging.critical("Total time: " + str(t3))                    
    return result

def calculate_price_for_demand(demand, date):
    '''
    Calculate price for the given demand from each store.
    This function assumes that the demand is a number for each category,
    e.g., 1 shirt, 2 sweaters. 
    '''
    
    logging.debug("Inside POST method of demowishlist")
    i = 1     
    result = ""           
    t1 = datetime.datetime.now()
    for store in stores:
        _wishlist = []
        result += "<p>" + str(store) 
        #date_ = datetime.date(2012, 1, 5)
        tt0 = datetime.datetime.now()
        stats_in_html_syntax, wishlist = create_sample_wishlist(i, store, date, cats, demand)
        tt1 = datetime.datetime.now()
        #result += "<br> " + stats_in_html_syntax
        result += "<br>" + str(wishlist) 
        orig_cost, total_cost, savings, shipping = find_price_of_wishlist_for_store(wishlist, 
                                                                                    store, i, date)
        tt2 = datetime.datetime.now()
        price_of_wishlist.append({"store": store,
                                  "orig_cost": orig_cost,
                                  "cost": total_cost,
                                  "savings": savings,
                                  "free_shipping": shipping,
                                  })
        result += "<br> Original cost " + str(orig_cost) + " Total cost after promo " \
               + str(total_cost) + " Savings " + str(savings) + " Shipping " + str(shipping) 
        print demand
        logging.critical( "RESULT:: " + str(store) + " " + str(orig_cost) + " " + str(total_cost) + " " + str(savings) + " " +\
             str(len(wishlist)) + " " + str(demand['sort_order']) + " " + str(wishlist))
        result += "</p>"
        i += 1
        time_sample_wishlist = tt1 - tt0
        time_price_for_wishlist = tt2 - tt1
        logging.debug("\t" + str(time_sample_wishlist) + " " + str(time_price_for_wishlist))
    t2 = datetime.datetime.now()
    t3 = t2 - t1
    logging.debug(t3)
    return (result, total_cost, savings, shipping)


def fill_demand(form):
    '''
    Fills up demand hash-table based on how many items the user picked
    for each category.
    '''
    shirts = form.cleaned_data['shirts']
    jeans = form.cleaned_data['jeans']
    skirts = form.cleaned_data['skirts']
    sweaters = form.cleaned_data['sweaters']
    gender = form.cleaned_data['gender']
    demand = {}
    demand['shirts'] = shirts
    demand['jeans'] = jeans
    demand['skirts'] = skirts
    demand['sweaters'] = sweaters
    demand['gender'] = gender
    return demand


def create_sample_wishlist(store_id, store_name, date, categories, demand):
    '''
    Construct a sample wishlist for store_name on date. demand[i] is
    the required number of items of categories[i]
    '''
    _wishlist = []
    result = ""
    for cat in categories:
        if demand[cat] > 0:
            tt0 = datetime.datetime.now()
            max, min, avg, num, item_list = find_items(store_id, store_name, cat, 'A', date)
            tt1 = datetime.datetime.now()
            result += "<br>Category " + str(cat) + " Max " + str(max) + " Min " \
                   + str(min) + " Avg " + str(avg) + " Num " + str(num) + "<br>"
            k = demand[cat]
            items = find_k_items(item_list, int(k), int(demand['sort_order']))
            tt2 = datetime.datetime.now()
            for item in items:            
                logging.debug(item)
                _wishlist.append( {"store": str(item.brand), 
                                   "category": str(item.cat1), 
                                   "price": float(item.price),
                                   "sale_price": float(item.saleprice)} )
            tt3 = datetime.datetime.now()
            logging.debug("\t\t"+ str(tt1 - tt0) + " " + str(tt2-tt1) + " " + str(tt3 - tt2))
            #print "Store: " + store_name + ": [" + str(max) + ", " + str(min) + ", " + str(avg) + "] #" + str(num)
    
    #print "Current wishlist: " + str(_wishlist)
    return (result, _wishlist)
    

def find_price_of_wishlist_for_store(wishlist, store_name, store_id, date_):
    '''
    Find the total price for the items in the wishlist from store_name and on date_
    '''
    promo_date = Promoinfo.objects.filter(d = date_)
    promo_store = promo_date.filter(store__id = store_id)
    promo = promo_store
    orig_cost, total_cost, savings, shipping = match.match(store_name, date_, copy.deepcopy(wishlist), promo)
    return (orig_cost, total_cost, savings, shipping)


def find_k_items(item_list, k, sort_order):
    '''
    Find  k items in the item_list
    based on the saleprice parameter
    and the sort_order defined in the forms
    
    '''
    try:
        if sort_order == MINIMUM:
            potential_items = item_list.order_by('saleprice')#.values() #filter(saleprice = min)
            return potential_items[0:k]
        if sort_order == MAXIMUM:
            potential_items = item_list.order_by('-saleprice')
            return potential_items[0:k]
        if sort_order == MEDIAN:
            potential_items = item_list.order_by('saleprice')
            logging.debug("ASSUMPTION: k is larger than the size of the set")
            #print potential_items[0:k]
            num = potential_items.count()
            mid = num/2
            start = mid - k/2 - 1
            end = mid + k/2 
            logging.critical("Total " + str(num) + " mid " + str(mid) + " k " + str(k) + " start " + str(start) + " end " + str(end))
            return potential_items[start:end]
    except Items.DoesNotExist:
        raise Http404

    return []

def find_qset(store_name, date, gender):
    
    try:
        qset = db_querysets[store_name]
            
        #if qset != None:
        return qset['data']
    except KeyError:
        day = datetime.timedelta(days=1)
        d_start = date - day
        d_end = date
        items_on_date = Items.objects.filter(insert_date__range = (d_start, d_end))
        potential_items = items_on_date.filter(brand__name = store_name)#.filter(insert_date = date)
        logging.debug("Number of items after store filter: " + str(len(potential_items)))
        # filter only if the category is specified
        if gender != 'A':
            potential_items2 = potential_items.filter(gender = gender)
            logging.debug("Size after gender filter: " + str(len(potential_items2)))
            potential_items = potential_items2
        qset = {'store_name': store_name,
                'data': potential_items,
                }
        db_querysets[store_name] = qset
        return potential_items

def find_items(store_id, store_name, category, gender, date):
          
    try:
        potential_items = find_qset(store_name, date, gender)
        # filter only if category is given
        potential_items3 = potential_items.filter(cat1__contains = category)
        logging.debug("Size after category filter: " + str(len(potential_items3)) + " " + category)
        potential_items = potential_items3
        
        max_ = potential_items.aggregate(Max('saleprice'))['saleprice__max']
        min_ = potential_items.aggregate(Min('saleprice'))['saleprice__min']
        avg_ = potential_items.aggregate(Avg('saleprice'))['saleprice__avg']
        num_ = potential_items.aggregate(Count('saleprice'))['saleprice__count']
        
        return max_, min_, avg_, num_, potential_items
    except Items.DoesNotExist:
        raise Http404
        
        
