# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django import forms
from polls.models import Promoinfo, Items
from django.db.models import Avg, Max, Min
import match



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

def result(request, total_cost, savings):
    html = "<html><body>Total cost: " + str(total_cost) + ". Total savings: " + str(savings) + "</body></html>"
    return HttpResponse(html)
    
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
                print potential_items3
                potential_items = potential_items3
                for items in potential_items:
                    print str(items.brand_id) + " " + str(items.cat1) + " " + str(items.gender) 
                print potential_items
                print "Max price: " + str(potential_items.aggregate(Max('price')))
                print "Min price: " + str(potential_items.aggregate(Min('price')))
                print "Avg price: " + str(potential_items.aggregate(Avg('price')))

            except Items.DoesNotExist:
                raise Http404
        
            print "Store " + str(store)
            print "Category " + str(item_category)
            print "Gender " + str(sex_category)
            
            return list_detail.object_list(
                                           request,
                                           queryset = potential_items,
                                           template_name = "items_list.html"
                                           #template_object_name = "items"
                                           #extra_context = {"items" : potential_items}
                                           )
            
            
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