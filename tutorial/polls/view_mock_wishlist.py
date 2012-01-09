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
                   (1, 1),
                   (2, 2),
                   (3, 3)
                   )
    shirts = forms.ChoiceField(choices = NUM_CHOICES)
    jeans = forms.ChoiceField(choices = NUM_CHOICES)
    skirts = forms.ChoiceField(choices = NUM_CHOICES)
    gender = forms.ChoiceField(choices = GENDER_CHOICES)
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
    
    if request.method == 'POST': # If the form has been submitted...
        form = DemoWishlist(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            shirts = form.cleaned_data['shirts']
            jeans = form.cleaned_data['jeans']
            skirts = form.cleaned_data['skirts']
            gender = form.cleaned_data['gender']
            #size = form.cleaned_data['size']
            #color = form.cleaned_data['color']
            #howmany = form.cleaned_data['howmany']
            date = datetime.date.today()
            stores = ("Express", "J.Crew")
            cats = ("shirts", "jeans", "skirts")
            print "Inside POST method of demowishlist"
            result = ""
            for store in stores:
                i = 1
                _wishlist = []
                result += "Store: " + str(store) + "<br>"
                for cat in cats:
                    max, min, avg, num, item_list = find_items(store, cat, 'A')
                    result += "<br>Category " + str(cat) + " Max " + str(max) + " Min " + str(min) + " Avg " + str(avg) + " Num " + str(num) + "<br>"
                    item = find_cheapest_item_any(item_list, min)
                    _wishlist.append( {"store": str(item.brand), 
                                       "category": str(item.cat1), 
                                       "price": float(item.price),
                                       "sale_price": float(item.saleprice)} )
                    print "Store: " + store + ": [" + str(max) + ", " + str(min) + ", " + str(avg) + "] #" + str(num)
                
                print "Current wishlist: " + str(_wishlist)
            
                date_ = datetime.date(2012, 1, 2)
                promo_date = Promoinfo.objects.filter(d = date_)
                print promo_date
                promo_store = promo_date.filter(store__id = i)
                promo = promo_store
                print promo
                orig_cost, total_cost, savings, shipping = match.match(stores[i], date_, copy.deepcopy(_wishlist), promo)
                result += "<br>\tOriginal cost " + str(orig_cost) + " Total cost after promo " + str(total_cost) + " Savings " + str(savings) + " Shipping " + str(shipping) + "<br><br>"
                i = i+1
            
            html = "<html><body><title>Summary of results</title>" 
            html += result
            html += "</body></html>"
            return HttpResponse(html)

    else:
        form = DemoWishlist()
    
    return render_to_response('mock_wishlist.html', {'form': form,}, context_instance=RequestContext(request))

def find_cheapest_item_any(item_list, min):
    try:
        potential_items = item_list.filter(saleprice = min)
        print potential_items[0]
        return potential_items[0]
    except Items.DoesNotExist:
        raise Http404

def find_items(store_name, category, gender):                
        try:
            potential_items = Items.objects.filter(brand__name = store_name)
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