# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django import forms
from polls.models import Promoinfo, Items, Brands, Categories, Demand, ItemList, ResultForDemand
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
from itertools import chain


logging.basicConfig(format='%(message)s', level=logging.DEBUG)
'''We simulate from 0-2 items selected from each category to create
    artificial wish lists. And then we calculate the prices for these
    wishlists to obtain insights. NUM_ITEMS_SIMULATED is the number of
    choices we have for each category.
'''
NUM_ITEMS_SIMULATED = 3

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
                   ('M', 'MALE'),
                   ('F', 'FEMALE'),
                   ('A', 'ALL'),
                   )
    NUM_CHOICES = (
                   (0, 0),
                   (1, 1),
                   (2, 2),
                   )
    SELECTION_CRITERIA = (
                          (MINIMUM, 'MINIMUM'),
                          (MAXIMUM, 'MAXIMUM'),
                          (MEDIAN, 'MEDIAN'),
                          
                          )
    shirts = forms.ChoiceField(choices = NUM_CHOICES, initial=1)
    jeans = forms.ChoiceField(choices = NUM_CHOICES, initial=1)
    skirts = forms.ChoiceField(choices = NUM_CHOICES, initial=1)
    sweaters = forms.ChoiceField(choices = NUM_CHOICES, initial=1)
    gender = forms.ChoiceField(choices = GENDER_CHOICES, initial=0)
    selection_criteria = forms.ChoiceField(choices = SELECTION_CRITERIA, initial=0)
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
    date = datetime.date.today()
    dd = datetime.timedelta(days=1)
    date2 = date - dd
    if request.method == 'POST': # If the form has been submitted...
        form = DemoWishlist(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            demand = fill_demand(form)
            
            demand_in_db = insert_demand_in_db(demand)
            val_str, val_cost, val_savings, val_free_shipping = calculate_price_for_demand(demand, date2, demand_in_db)
            result += val_str    
    else:
        form = DemoWishlist()
        #result += calculate_price_for_simulated_demands(MAXIMUM, date)
    logging.debug(price_of_wishlist)    
    return render_to_response('mock_wishlist.html', 
                              {'form': form, 
                               #'results': result,
                               'price_wishlist': price_of_wishlist,}, 
                              context_instance=RequestContext(request))

def fill_db(request):
    gender = ['M', 'F', 'A']
    ordering = [MINIMUM, MAXIMUM, MEDIAN]
    date1 = datetime.date.today()
    dd = datetime.timedelta(days=1)
    date = date1 - dd
    for g in gender:
        for order in ordering:
            calculate_price_for_simulated_demands(order, date, g)
            logging.critical("Done with Gender: " + g + " order " + str(order))
    html = "<html><body>Done, thanks for populating the results DB.</body></html>"
    return HttpResponse(html)

def calculate_price_for_simulated_demands(sort_order, date, gender):
    num = 0
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
                        demand['gender'] = gender
                        demand['sort_order'] = sort_order
                        demand_in_db = insert_demand_in_db(demand)
                        logging.debug(demand)
                        num += 1
                        result += "<br>==================================<br>"
                        result += "<br>=== DEMAND: " + str(demand) + "<br>"
                        val_str, val_cost, val_savings, val_free_shipping = calculate_price_for_demand(demand, date, demand_in_db)
                        logging.critical("Done with demand " + str(num))
                        result += val_str
    t2 = datetime.datetime.now()
    t3 = t2 - t1
    logging.critical("Total time: " + str(t3))                    
    return result

def insert_demand_in_db(demand):
    total = int(demand['shirts']) + int(demand['sweaters']) + int(demand['skirts']) + int(demand['jeans'])
    d = Demand.objects.filter(num_shirts = int(demand['shirts']),
                               num_sweaters = int(demand['sweaters']),
                               num_skirts = int(demand['skirts']),
                               num_jeans = int(demand['jeans']),
                               gender = demand['gender'],
                               total_items = total)
    if d.count() > 0:
        return d[0]
    else:
        d = Demand(num_shirts = int(demand['shirts']),
                   num_sweaters = int(demand['sweaters']),
                   num_skirts = int(demand['skirts']),
                   num_jeans = int(demand['jeans']),
                   gender = demand['gender'],
                   total_items = total)
        d.save()
        return d

def initialize_itemlist_entry(w):
    w.total_items = 0
    w.item1 = None
    w.item2 = None
    w.item3 = None
    w.item4 = None
    w.item5 = None
    w.item6 = None
    w.item7 = None
    w.item8 = None
    w.item9 = None
    w.item10 = None
    w.item11 = None
    w.item12 = None
    w.item13 = None
    w.item14 = None
    w.item15 = None
    w.item16 = None
    

def insert_itemlist_in_db(list_of_querysets):
    w = ItemList()
    initialize_itemlist_entry(w)
    print list_of_querysets
    size = len(list_of_querysets)
    
    if len(list_of_querysets) == 0:
        return w
    result_list = list_of_querysets[0]
    for i in range(0, size):
        l = list_of_querysets[i]
        if l != None:
            result_list = chain(result_list, l)
    
    if result_list == None:
        print "Result_list is NULL: " + str(result_list)
        return w

    itemlist_queryset = list(result_list)
        
    num = len(itemlist_queryset)
    print num
    w.total_items = num
    
    print itemlist_queryset
    if num == 1:
        w.item1 = itemlist_queryset[0]
    elif num == 2:
        w.item1 = itemlist_queryset[0]
        w.item2 = itemlist_queryset[1]
    elif num == 3:
        w.item1 = itemlist_queryset[0]
        w.item2 = itemlist_queryset[1]
        w.item3 = itemlist_queryset[2]
    elif num == 4:
        w.item1 = itemlist_queryset[0]
        w.item2 = itemlist_queryset[1]
        w.item3 = itemlist_queryset[2]
        w.item4 = itemlist_queryset[3]
    elif num == 5:
        w.item1 = itemlist_queryset[0]
        w.item2 = itemlist_queryset[1]
        w.item3 = itemlist_queryset[2]
        w.item4 = itemlist_queryset[3]
        w.item5 = itemlist_queryset[4]
    elif num == 6:
        w.item1 = itemlist_queryset[0]
        w.item2 = itemlist_queryset[1]
        w.item3 = itemlist_queryset[2]
        w.item4 = itemlist_queryset[3]
        w.item5 = itemlist_queryset[4]
        w.item6 = itemlist_queryset[5]
    elif num == 7:
        w.item1 = itemlist_queryset[0]
        w.item2 = itemlist_queryset[1]
        w.item3 = itemlist_queryset[2]
        w.item4 = itemlist_queryset[3]
        w.item5 = itemlist_queryset[4]
        w.item6 = itemlist_queryset[5]
        w.item7 = itemlist_queryset[6]
    elif num == 8:
        w.item1 = itemlist_queryset[0]
        w.item2 = itemlist_queryset[1]
        w.item3 = itemlist_queryset[2]
        w.item4 = itemlist_queryset[3]
        w.item5 = itemlist_queryset[4]
        w.item6 = itemlist_queryset[5]
        w.item7 = itemlist_queryset[6]
        w.item8 = itemlist_queryset[7]
    logging.debug("Creating entry in ItemList table: " + str(w))
    w.save()
    return w
        
def insert_result_in_db(demand_, itemlist_, date_, 
                        cost_without_promo, cost_with_promo, 
                        free_shipping_, store_name_, sort_order):
    logging.debug("Creating entry in ResultForDemand table")
    r = ResultForDemand(demand = demand_,
                        itemlist = itemlist_,
                        date = date_,
                        total_without_sale = cost_without_promo,
                        total_with_sale = cost_with_promo,
                        free_shipping = free_shipping_,
                        store_name = None,
                        store_string = store_name_,
                        item_selection_metric = sort_order,
                         )
    r.save()
    logging.debug(r)
    return r


def find_result_for_demand(dem, date, sort_order):
    
    qset = ResultForDemand.objects.filter(demand = dem, date__contains = date, item_selection_metric = sort_order)
    logging.critical("For dem " + str(dem) + " found " + str(qset.count()))
    if qset.count() > 0:
        return qset
    else:
        return None
    
def calculate_price_for_demand(demand, date, demand_in_db):
    '''
    Calculate price for the given demand from each store.
    This function assumes that the demand is a number for each category,
    e.g., 1 shirt, 2 sweaters. 
    '''
    
    logging.debug("Inside POST method of demowishlist")
    
    results_for_demand = find_result_for_demand(demand_in_db, date, int(demand['sort_order']))
        
    if results_for_demand != None:
        for r in results_for_demand:
            price_of_wishlist.append({"store": r.store_string,
                                      "orig_cost": r.total_without_sale,
                                      "cost": r.total_with_sale,
                                      "savings": (r.total_without_sale-r.total_with_sale),
                                      "free_shipping": r.free_shipping,
                                      })
        return ("Hello", 0,0, False)
    else:
    
        i = 1     
        result = ""           
        t1 = datetime.datetime.now()
        for store in stores:
            _wishlist = []
            result += "<p>" + str(store) 
            #date_ = datetime.date(2012, 1, 5)
            tt0 = datetime.datetime.now()
            stats_in_html_syntax, wishlist, wishlist_queryset = create_sample_wishlist(i, store, date, cats, demand)
            tt1 = datetime.datetime.now()
            #result += "<br> " + stats_in_html_syntax
            result += "<br>" + str(wishlist) 
            orig_cost, total_cost, savings, shipping = find_price_of_wishlist_for_store(wishlist, 
                                                                                        store, i, date)
            w = insert_itemlist_in_db(wishlist_queryset)
            r = insert_result_in_db(demand_in_db, w, date, orig_cost, total_cost, shipping, store, int(demand['sort_order']))
            tt2 = datetime.datetime.now()
            price_of_wishlist.append({"store": store,
                                      "orig_cost": orig_cost,
                                      "cost": total_cost,
                                      "savings": savings,
                                      "free_shipping": shipping,
                                      })
            result += "<br> Original cost " + str(orig_cost) + " Total cost after promo " \
                   + str(total_cost) + " Savings " + str(savings) + " Shipping " + str(shipping) 
            logging.debug(str(demand))
            logging.debug( "RESULT:: " + str(store) + " " + str(orig_cost) + " " + str(total_cost) + " " + str(savings) + " " +\
                 str(len(wishlist)) + " " + str(demand['sort_order']) + " " + str(wishlist))
            result += "</p>"
            i += 1
            time_sample_wishlist = tt1 - tt0
            time_price_for_wishlist = tt2 - tt1
            logging.debug("\t" + str(time_sample_wishlist) + " " + str(time_price_for_wishlist))
        t2 = datetime.datetime.now()
        t3 = t2 - t1
        logging.critical(t3)
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
    sort_order = form.cleaned_data['selection_criteria']

    demand = {}
    demand['shirts'] = shirts
    demand['jeans'] = jeans
    demand['skirts'] = skirts
    demand['sweaters'] = sweaters
    demand['gender'] = gender
    demand['sort_order'] = sort_order
    return demand


def combine_qsets(qset1, qset2):
    if qset1 == None:
        return qset2
    if qset2 == None:
        return qset1
    return qset1 | qset2
    


def create_sample_wishlist(store_id, store_name, date, categories, demand):
    '''
    Construct a sample wishlist for store_name on date. demand[i] is
    the required number of items of categories[i]
    '''
    _wishlist = []
    result = ""
    item_queryset = []#Items.objects.none()
    for cat in categories:
        if demand[cat] > 0:
            tt0 = datetime.datetime.now()
            G = demand['gender']
            max, min, avg, num, item_list = find_items(store_id, store_name, cat, G, date)
            tt1 = datetime.datetime.now()
            result += "<br>Category " + str(cat) + " Max " + str(max) + " Min " \
                   + str(min) + " Avg " + str(avg) + " Num " + str(num) + "<br>"
            k = demand[cat]
            items = find_k_items(item_list, int(k), int(demand['sort_order']))
            item_queryset.append(items)
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
    return (result, _wishlist, item_queryset)
    

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
            if num < k*2:
                ''' SIMPLIFYING ASSUMPTION: if we have less than twice the k elements, we use all '''
                return potential_items
            else:
                if num % 2 == 0:
                    mid = num/2
                else:
                    mid = (num+1)/2
                start = mid - k/2 
                end = mid + k/2
                if k < 2:
                    end += 1 
                how_many = end - start
                assert how_many == k
                logging.debug("Total " + str(num) + " mid " + str(mid) + " k " + str(k) + " start " + str(start) + " end " + str(end))
                return potential_items[start:end]
    except Items.DoesNotExist:
        raise Http404

    return []

def find_qset(store_name, date, gender, category):
    
    try:
        qset = db_querysets[store_name + category + gender]
            
        #if qset != None:
        return qset['data']
    except KeyError:
        logging.critical("Didn't find: " + store_name + " " + str(date) + " " + category)
        start_night = datetime.time(0)
        mid_night = datetime.time(23, 59, 59)
        #day = datetime.timedelta(hours=23, minutes=59, seconds=59)
        d_start = datetime.datetime.combine(date, start_night)
        d_end = datetime.datetime.combine(date, mid_night)
        items_on_date = Items.objects.filter(insert_date__range = (d_start, d_end))
        print date
        print "Number of items after date filter: " + str(len(items_on_date))
        logging.debug("QUERY: " + str(items_on_date.query))
        potential_items = items_on_date.filter(brand__name = store_name)#.filter(insert_date = date)
        logging.debug("Number of items after store filter: " + str(len(potential_items)))
        print "Number of items after store filter: " + str(len(potential_items))
        # filter only if the category is specified
        if gender != 'A':
            potential_items2 = potential_items.filter(gender = gender)
            logging.debug("Size after gender filter: " + str(len(potential_items2)))
            print "Size after gender filter: " + str(len(potential_items2))
            potential_items = potential_items2
        
        potential_items3 = potential_items.filter(cat1__contains = category)
        logging.debug("Size after category filter: " + str(len(potential_items3)) + " " + category)
        print "Size after category filter: " + str(len(potential_items3)) + " " + category
        potential_items = potential_items3
        
        qset = {'store_name': store_name,
                'category': category,
                'data': potential_items,
                }
        
        db_querysets[store_name + category + gender] = qset
        #print potential_items[0]
        return potential_items

def find_items(store_id, store_name, category, gender, date):
          
    try:
        potential_items = find_qset(store_name, date, gender, category)
        # filter only if category is given
        
        '''
        max_ = potential_items.aggregate(Max('saleprice'))['saleprice__max']
        min_ = potential_items.aggregate(Min('saleprice'))['saleprice__min']
        avg_ = potential_items.aggregate(Avg('saleprice'))['saleprice__avg']
        num_ = potential_items.aggregate(Count('saleprice'))['saleprice__count']
        '''
        max_ = 0
        min_ = 0
        avg_ = 0
        num_ = potential_items.count()
        return max_, min_, avg_, num_, potential_items
    except Items.DoesNotExist:
        raise Http404
        
        
