# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django import forms
from polls.models import Promoinfo, Items
from django.db.models import Avg, Max, Min, Count
import match
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


item_list_results_hash_table = {}

selected_items_id_list = {}
selected_items = {}

NUM_COLUMNS_TABLE_TEMPLATE = 5

class Wishlist(forms.Form):
    
    
    STORE_CHOICES = (
                     ("J.Crew", 'J.CREW'),
                     ("Express", 'EXPRESS'),
                     )
    GENDER_CHOICES = (
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
    
    
    store = forms.ChoiceField(choices = STORE_CHOICES)
    item_category = forms.ChoiceField(choices = ITEM_CATEGORY_CHOICES)
    sex_category = forms.ChoiceField(choices = GENDER_CHOICES)
    size = forms.IntegerField()
    color = forms.IntegerField()
    howmany = forms.IntegerField()

    ''' QUESTION 
    1. A user must be able to select multiple items of different category from the same store
    2. A user must be able to choose items from different stores.
    
    '''
def add_item_to_selected_items_list(request, wishlist_id_, item_id_, page_id_):
    print "Adding item " + str(item_id_) + " to wishlist id " + str(wishlist_id_)
    selected_items_id_list[int(wishlist_id_)].append(item_id_)
    selected_items[int(wishlist_id_)] = []
    print selected_items_id_list[int(wishlist_id_)]
    print page_id_
    return HttpResponseRedirect("/wishlist/" + wishlist_id_ + "/?page=" + str(page_id_))


def apply_discount(request, wishlist_id_):
    item_list = selected_items[int(wishlist_id_)]
    #store_name_ = "J.Crew"
    # Assuming all items are from the same store. 
    # TODO: fix this when items are selected from multiple stores
    store_name = item_list[0]['store']
    date_ = datetime.date.today()
    promo = Promoinfo.objects.filter(d = date_)
    orig_cost, total_cost, savings, shipping = match.match(store_name, date_, item_list, promo)
    html = "<html><body>Total cost: $" + str(orig_cost) + ". With promotion: $" + str(total_cost) + " We saved $" + \
        str(savings) + " Free shipping?" + str(shipping) + "</body></html>" 
    return HttpResponse(html)

def show_selected_items(request, wishlist_id_):
    selected_items_id = selected_items_id_list[int(wishlist_id_)]
    original_item_list = item_list_results_hash_table[int(wishlist_id_)]

    #print "Show selected items: " + str(result_list)
    html ="<html><body><title>Selected Items</title>"
    html += "<h2>Your Selected Items List.</h2>"
    html += "<ul>"
    itemlist = [] 
    for id_ in selected_items_id:
        qset = original_item_list.filter(id = id_)
        print id_
        print qset
        for items in qset:
            print str(items.brand) + " " + str(items.cat1) + " " + str(items.gender) + " " + str(items.price)
            #selected_items[(int(wishlist_id_))].append(items)
            html += "<li> " + str(items.brand) + " " + str(items.cat1) + " " + str(items.gender) \
                    + " " + str(items.price) + " " + str(items.saleprice) + "</li>"
            itemlist.append( {"store": str(items.brand), 
                          "category": str(items.cat1), 
                          "price": float(items.price),
                          "sale_price": float(items.saleprice)} )
    selected_items[int(wishlist_id_)] = itemlist
    html += "<h3>Apply discounts to save money? Click <a href=\"apply_discount\">here</a></h3>"
    html += "</body></html>"
    return HttpResponse(html)
    '''
    THIS DIDN"T WORK SINCE result_list is not a queryset.
    This resulted in list doesn't have a _clone method.
    return list_detail.object_list(
                                           request,
                                           queryset = result_list,
                                           template_name = "items_list.html"
                                           #template_object_name = "items"
                                           #extra_context = {"items" : potential_items}
                                           )
    '''
    
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def result(max_, min_, avg_, num_, id_):
    html = "<html><body><title>Summary of results</title>" + \
           "<p>We found " + str(num_) + " items satisfying your query. " + \
           "<a href=\"" + str(id_) + "\">View items?</a></p>" + \
           "<p>Max price: " + str(max_) + ". Min: " + str(min_) + ". Avg " + str(avg_) + "</p>" + \
           "</body></html>"
    return HttpResponse(html)

def calculate_selected_items(wishlist_id_):
    return len(selected_items_id_list[int(wishlist_id_)])
    
def render_result_list(request, id_):
    
    int_id = int(id_)
    print "Argument " + id_ + " int_id " + str(int_id)
    #return current_datetime(request)
    
    result_list = item_list_results_hash_table[int_id]
    paginator = Paginator(result_list, 25)
    page = request.GET.get('page')
    if page is None:
        page = 1
    try:
        page_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_list = paginator.page(paginator.num_pages)
    print "Printing page_list here: " + str(page_list)
    return list_detail.object_list(
                                           request,
                                           queryset = result_list,
                                           template_name = "items_list.html",
                                           paginate_by = 25,
                                           #template_name = "items_list.html"
                                           #template_object_name = "items"
                                           extra_context = {'page_list': page_list,
                                                            'num_selected': 5}
                                           )

def render_result_table(request, id_):
    
    int_id = int(id_)
    print "Argument " + id_ + " int_id " + str(int_id)
    #return current_datetime(request)
    
    result_list = item_list_results_hash_table[int_id]
    paginator = Paginator(result_list, 25)
    page = request.GET.get('page')
    if page is None:
        page = 1
    try:
        page_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_list = paginator.page(paginator.num_pages)
    print "Printing page_list here: " + str(page_list)
    try:
        num_selected = calculate_selected_items(id_)
    except Exception:
        num_selected = 0
        
    print num_selected
    return list_detail.object_list(
                                           request,
                                           queryset = result_list,
                                           template_name = "items_table.html",
                                           paginate_by = 25,
                                           #template_name = "items_list.html"
                                           #template_object_name = "items"
                                           extra_context = {"page_list" : page_list,
                                                            "num_columns" : NUM_COLUMNS_TABLE_TEMPLATE,
                                                            "num_selected": num_selected}
                                           )

    
def wishlist(request):
    if request.method == 'POST': # If the form has been submitted...
        form = Wishlist(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            store = form.cleaned_data['store']
            item_category = form.cleaned_data['item_category']
            gender = form.cleaned_data['sex_category']
            size = form.cleaned_data['size']
            color = form.cleaned_data['color']
            howmany = form.cleaned_data['howmany']
            date = datetime.date.today()
            
            try:
                potential_items = Items.objects.filter(brand__name = store)
                # filter only if the category is specified
                if gender != 'A':
                    potential_items2 = potential_items.filter(gender = gender)
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
            print "Gender " + str(gender)
            
            id_ = int(num_)
            print id_
            item_list_results_hash_table[id_] = potential_items
            selected_items_id_list[id_] = []
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