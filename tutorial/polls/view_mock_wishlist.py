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

class DemoWishlist(forms.Form):
    
    
    STORE_CHOICES = (
                     ("J.Crew", 'J.CREW'),
                     ("Express", 'EXPRESS'),
                     )
    
    
    ITEM_CATEGORY_CHOICES = (
                             ('shirts', 'SHIRTS'),
                             ('pants', 'PANTS'),
                             ('sweaters', 'SWEATERS'),
                             ('jeans', 'JEANS'),
                             ('outerwear', 'OUTERWEAR'),
                             ('underwear', 'UNDERWEAR'),
                             ('everything', 'EVERYTHING')
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

stores = ("Express", "J.Crew", "Banana Republic")
cats = ("shirts", "jeans", "skirts", "sweaters")    

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

    if request.method == 'POST': # If the form has been submitted...
        form = DemoWishlist(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            demand = fill_demand(form)
            date = datetime.date.today()
            result += calculate_price_for_demand(demand, date)    
    else:
        form = DemoWishlist()
        result += calculate_price_for_simulated_demands()
    
    return render_to_response('mock_wishlist.html', 
                              {'form': form, 'results': result,}, 
                              context_instance=RequestContext(request))

def calculate_price_for_simulated_demands():
    num = 0
    date = datetime.date.today()
    result = ""
    for i in range(0, 3):
        for j in range(0,3):
            for k in range(0,3):
                for l in range(0,3):
                        demand = {}
                        demand[cats[0]] = i
                        demand[cats[1]] = j
                        demand[cats[2]] = k
                        demand[cats[3]] = l
                        print demand
                        num += 1
                        result += "<br>==================================<br>"
                        result += "<br>=== DEMAND: " + str(demand) + "<br>"
                        result += calculate_price_for_demand(demand, date)
                        
    return result

def calculate_price_for_demand(demand, date):
    '''
    Calculate price for the given demand from each store.
    This function assumes that the demand is a number for each category,
    e.g., 1 shirt, 2 sweaters. 
    '''
    
    print "Inside POST method of demowishlist"
    i = 1     
    result = ""           
    for store in stores:
        _wishlist = []
        result += "<p>" + str(store) 
        #date_ = datetime.date(2012, 1, 5)
        stats_in_html_syntax, wishlist = create_sample_wishlist(store, date, cats, demand)
        #result += "<br> " + stats_in_html_syntax
        result += "<br>" + str(wishlist) 
        orig_cost, total_cost, savings, shipping = find_price_of_wishlist_for_store(wishlist, 
                                                                                    store, i, date)
        result += "<br> Original cost " + str(orig_cost) + " Total cost after promo " \
               + str(total_cost) + " Savings " + str(savings) + " Shipping " + str(shipping) 
        result += "</p>"
        i += 1
    return result


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


def create_sample_wishlist(store_name, date, categories, demand):
    '''
    Construct a sample wishlist for store_name on date. demand[i] is
    the required number of items of categories[i]
    '''
    _wishlist = []
    result = ""
    for cat in categories:
        if demand[cat] > 0:
            max, min, avg, num, item_list = find_items(store_name, cat, 'A', date)
            result += "<br>Category " + str(cat) + " Max " + str(max) + " Min " \
                   + str(min) + " Avg " + str(avg) + " Num " + str(num) + "<br>"
            k = demand[cat]
            items = find_cheapest_k_items(item_list, int(k))
            for item in items:            
                print item
                _wishlist.append( {"store": str(item.brand), 
                                   "category": str(item.cat1), 
                                   "price": float(item.price),
                                   "sale_price": float(item.saleprice)} )
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


def find_cheapest_k_items(item_list, k):
    '''
    Find cheapest k items in the item_list
    based on the saleprice parameter
    '''
    try:
        potential_items = item_list.order_by('saleprice')#.values() #filter(saleprice = min)
        print "ASSUMPTION: k is larger than the size of the set"
        #print potential_items[0:k]
        return potential_items[0:k]
    except Items.DoesNotExist:
        raise Http404

    return []


def find_items(store_name, category, gender, date):         
    '''
    Search in the item database for items from category, gender, store_name
    and with specific insertion date
    '''       
    try:
        day = datetime.timedelta(days=1)
        d_start = date - day
        d_end = date
        items_on_date = Items.objects.filter(insert_date__range = (d_start, d_end))
        potential_items = items_on_date.filter(brand__name = store_name)#.filter(insert_date = date)
        print "Number of items after store filter: " + str(len(potential_items))
        # filter only if the category is specified
        if gender != 'A':
            potential_items2 = potential_items.filter(gender = gender)
            print "Size after gender filter: " + str(len(potential_items2))
            potential_items = potential_items2
        # filter only if category is given
        potential_items3 = potential_items.filter(cat1__contains = category)
        print "Size after category filter: " + str(len(potential_items3)) + " " + category
        potential_items = potential_items3
        
        max_ = potential_items.aggregate(Max('saleprice'))['saleprice__max']
        min_ = potential_items.aggregate(Min('saleprice'))['saleprice__min']
        avg_ = potential_items.aggregate(Avg('saleprice'))['saleprice__avg']
        num_ = potential_items.aggregate(Count('saleprice'))['saleprice__count']
        return max_, min_, avg_, num_, potential_items
    except Items.DoesNotExist:
        raise Http404
        
        
