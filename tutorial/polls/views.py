# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django import forms
from polls.models import Promoinfo, Items
from django.db.models import Avg, Max, Min, Count
import match

item_list_results_hash_table = {}

class Wishlist(forms.Form):
    
    
    STORE_CHOICES = (
                     ("J.Crew", 'J.CREW'),
                     ("Express", 'EXPRESS'),
                     )
    SEX_CHOICES = (
                   ('M', 'MALE'),
                   ('F', 'FEMALE'),
                   ('A', 'ALL'),
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
    
    #store = forms.CharField(max_length=100, choices = STORE_CHOICES)
    store = forms.ChoiceField(choices = STORE_CHOICES)
    item_category = forms.ChoiceField(choices = ITEM_CATEGORY_CHOICES)
    sex_category = forms.ChoiceField(choices = SEX_CHOICES)
    size = forms.IntegerField()
    color = forms.IntegerField()
    howmany = forms.IntegerField()

    ''' QUESTION 
    1. A user must be able to select multiple items of different category from the same store
    2. A user must be able to choose items from different stores.
    
    '''

    
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def result(max_, min_, avg_, num_, id_):
    html = "<html><body><title>Summary of results</title>" + \
           "<p>We found " + str(num_) + " items satisfying your query. " + \
           "<a href=\"" + str(id_) + "\">View items?</a></p>" + \
           "<p>Max cost: " + str(max_) + ". Min: " + str(min_) + ". Avg " + str(avg_) + "<p></body></html>"
    return HttpResponse(html)
    
def render_result_list(request, id_):
    print "Argument " + id_
    int_id = int(id_)
    print "Argument " + id_ + " int_id " + str(int_id)
    #return current_datetime(request)
    
    result_list = item_list_results_hash_table[int_id]
    return list_detail.object_list(
                                           request,
                                           queryset = result_list,
                                           template_name = "items_list.html"
                                           #template_object_name = "items"
                                           #extra_context = {"items" : potential_items}
                                           )
    
def wishlist(request):
    if request.method == 'POST': # If the form has been submitted...
        form = Wishlist(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            store = form.cleaned_data['store']
            item_category = form.cleaned_data['item_category']
            sex_category = form.cleaned_data['sex_category']
            size = form.cleaned_data['size']
            color = form.cleaned_data['color']
            howmany = form.cleaned_data['howmany']
            date = datetime.date.today()
            
            try:
                potential_items = Items.objects.filter(brand__name = store)
                # filter only if the category is specified
                if sex_category != 'A':
                    potential_items2 = potential_items.filter(gender = sex_category)
                    print potential_items2
                    potential_items = potential_items2
                # filter only if category is given
                potential_items3 = potential_items.filter(cat1__contains = item_category)
                #print potential_items3
                potential_items = potential_items3
                for items in potential_items:
                    print str(items.brand_id) + " " + str(items.cat1) + " " + str(items.gender) + " " + str(items.price)
                #print potential_items
                max_ = potential_items.aggregate(Max('price'))['price__max']
                #print max['price__max']
                min_ = potential_items.aggregate(Min('price'))['price__min']
                avg_ = potential_items.aggregate(Avg('price'))['price__avg']
                num_ = potential_items.aggregate(Count('price'))['price__count']
                print "Max price: " + str(max_) + " Min price " + str(min_) + " Avg price " + str(avg_) + " Count " + str(num_)

            except Items.DoesNotExist:
                raise Http404
        
            print "Store " + str(store)
            print "Category " + str(item_category)
            print "Gender " + str(sex_category)
            
            id_ = int(num_)
            print id_
            item_list_results_hash_table[id_] = potential_items
            #result_item_list[form] = potential_items
            return result(max_, min_, avg_, num_, id_)
            '''
            return list_detail.object_list(
                                           request,
                                           queryset = potential_items,
                                           template_name = "items_list.html"
                                           #template_object_name = "items"
                                           #extra_context = {"items" : potential_items}
                                           )
            
            '''
            '''    
            wish = []
            wish.append(store)
            wish.append(item_category)
            wish.append(sex_category)
            wish.append(size)
            wish.append(howmany)
            #print "Store name: " + str(store)
            #print wish
            #total_cost, savings = match.match(store, date, wish)
            total_cost = 200
            savings = 50
            return result(request, total_cost, savings)
            
            #return HttpResponseRedirect(reverse('/result/', args=(total_cost, savings))) # Redirect after POST
            '''
    else:
        form = Wishlist() # An unbound form
    print form
    
    return render_to_response('wishlist.html', {
        'form': form,
    })