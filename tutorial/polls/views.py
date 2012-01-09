# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django import forms
from polls.models import Promoinfo, Items, Brands, Categories
from django.db.models import Avg, Max, Min, Count
import match
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

class Wishlist(forms.Form):
    
    
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
    
def weather_chart_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
           series=
            [{'options': {
               'source': Promoinfo.objects.all()},
              'terms': [
                'store',
                'validity',
                'free_shipping_lower_bound']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = weatherdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'store': [
                    'validity',
                    'validity']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Weather Data of Boston and Houston'},
               'xAxis': {
                    'title': {
                       'text': 'Month number'}}})

    #Step 3: Send the chart object to the template.
    return render_to_response('show_chart.html', {'weatherchart': cht})
    
class WishlistForm(forms.Form):
    
    gender = ChoiceField(choices = GENDER_CHOICES, required=False)
    brands = ModelChoiceField(queryset=Brands.objects.all(), empty_label="Select", required=False)
 
    def __init__(self,*args,**kwargs):
        br_id = kwargs.pop('br_id')
        super(WishlistForm, self).__init__(*args, **kwargs)
        
        if (br_id > 0):
            self.fields['categories'] = ModelChoiceField(queryset=Categories.objects.filter(brand=br_id), empty_label="Select", required=False)
       
        print "Inside __init__: " + str(self.fields) + str(br_id)
    
def add_item_to_selected_items_list(request, wishlist_id_, item_id_, page_id_):
    print "Adding item " + str(item_id_) + " to wishlist id " + str(wishlist_id_)
    selected_items_id_list[int(wishlist_id_)].append(item_id_)
    selected_items[int(wishlist_id_)] = []
    print selected_items_id_list[int(wishlist_id_)]
    print page_id_
    return HttpResponseRedirect("/wishlist/" + wishlist_id_ + "/?page=" + str(page_id_))

def compare_promo(request):
    promos = Promoinfo.objects.filter(d__gte = datetime.date(2012, 1, 1))
    for promo in promos:
        print promo
    
    
def pricerange_result(br_name, cat, max_, min_, avg_, num_):
    html = "<p>In " + br_name + ", we found " + str(num_) + " items in category: " + cat + ". Max price: " + str(max_) + ". Min: " + str(min_) + ". Avg " + str(avg_) + "</p>\n"
           #"<a href=\"" + str(id_) + "\">View items?</a></p>" + \
           # "<html><body><title>Summary of results</title>" + \
           #"</body></html>"
    return html

def compare_pricerange(request):
    # from today's items, compare across stores price range, and print on return
    
    # Pseudo-code
    # for categories of interest:
    #     for i = 1 to total_brand_num:
    #         Get unique items from today's info  
    # for unique items from today's info:
    #     Calculate min, max, avg, std. dev, median of price and saleprice
    #     Return this info to client (as text first, and then a plot)
    #   
    
    # Get today's date
    date_today = datetime.date.today()
    
    # Across brands
    br_info = Brands.objects.all()
    
    html_to_render = "<html><body><title>Summary of results</title>\n"
    
    avgnum = {}
    chart_max = 0
    for i in ['shirts', 'jeans', 'skirts']: # Get this as input from User?
        avgnumarr = []
        for j in range(0,len(br_info)-1):
            # Currently, we only get items that match cat1. What about others?
            it1 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[j].id).filter(cat1__contains=i)
            it2 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[j].id).filter(cat2__contains=i)
            it3 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[j].id).filter(cat3__contains=i)
            it4 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[j].id).filter(cat4__contains=i)
            it5 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[j].id).filter(cat5__contains=i)
            
            # Find unique products that include i in any of cat1 to cat5
            it = it1 | it2 | it3 | it4 | it5
            
            it_max = it.aggregate(Max('price'))['price__max']
            it_min = it.aggregate(Min('price'))['price__min']
            it_avg = it.aggregate(Avg('price'))['price__avg']
            it_num = it.aggregate(Count('price'))['price__count']
            print date_today, br_info[j].name, i, it_num, it_min, it_avg, it_max
            avgnumarr.append(it_avg)
            if it_avg > chart_max:
                chart_max = it_avg
        avgnum[i] = avgnumarr
            #html_to_render += pricerange_result(br_info[j].name, i, it_max, it_min, it_avg, it_num)
    
    #html_to_render += "</body></html>"
    #print html_to_render
    
    print avgnum
    
    #line = Line([[0,0,0,0,0,0],[0,5,10,7,12,6],[35,25,45,47,24,46],[15,40,30,27,39,54],[70,55,63,59,80,60]],encoding='text',series=1)
    #line.scale(0,100,-50,100)
    #line.marker('F','',1,'1:4',20)
    #line.axes('xy')
    #line.title('Fucking title')
    
    
    bar = VerticalBarGroup([avgnum['jeans'], 
                            avgnum['shirts'], 
                            avgnum['skirts']], 
                           encoding='text') 
    bar.color('blue', 'red', 'green')
    bar.axes('xy')
    bar.title('Price Comparison')
    bar.scale(0,chart_max+10)
    #bar.bar(17,15)
    #bar.size(500,200)
    #bar.size(600,400)
    #bar.axes('xy')
    bar.axes.label(0, 'Express', 'JCrew')
    bar.legend('Jeans', 'Shirts', 'Skirts')
    #bar.marker('N*cEUR1*','black',0,-1,11)
    bar.axes.range(1, 0.0,chart_max+10)
    #bar.title('Price comparison across stores','00cc00',12)
    return render_to_response('show_pricecomp.html', {'bar': bar}) #{'pie' : pie, 'scatter': scatter, 'bar': bar})

    #return HttpResponse(html_to_render)
    
def apply_discount(request, wishlist_id_):
    item_list = selected_items[int(wishlist_id_)]
    #store_name_ = "J.Crew"
    # Assuming all items are from the same store. 
    # TODO: fix this when items are selected from multiple stores
    store_name = item_list[0]['store']
    date_ = datetime.date.today()
    #promo = Promoinfo.objects.filter(d = date_)
    promo_date = Promoinfo.objects.filter(d__gte = datetime.date(2012, 1, 1))
    print promo_date
    promo_store = promo_date.filter(store = 1)
    promo = promo_store
    orig_cost, total_cost, savings, shipping = match.match(store_name, date_, copy.deepcopy(item_list), promo)
    html = "<html><body>Total cost: $" + str(orig_cost) + ". With promotion: $" + str(total_cost) + " We saved $" + \
        str(savings) + " Free shipping?" + str(shipping) + "</body></html>" 
    print html
    
    promo_store = promo_date.filter(store = 2)
    promo = promo_store
    orig_cost, total_cost, savings, shipping = match.match(store_name, date_, copy.deepcopy(item_list), promo)
    html += "<html><body>Total cost: $" + str(orig_cost) + ". With promotion: $" + str(total_cost) + " We saved $" + \
        str(savings) + " Free shipping?" + str(shipping) + "</body></html>" 
    print html

    promo_store = promo_date.filter(store = 3)    
    promo = promo_store
    orig_cost, total_cost, savings, shipping = match.match(store_name, date_, copy.deepcopy(item_list), promo)
    html += "<html><body>Total cost: $" + str(orig_cost) + ". With promotion: $" + str(total_cost) + " We saved $" + \
        str(savings) + " Free shipping?" + str(shipping) + "</body></html>" 
    print html    
    
    return HttpResponse(html)



def show_selected_items_new(request, wishlist_id_):
    selected_items_id = selected_items_id_list[int(wishlist_id_)]
    original_item_list = item_list_results_hash_table[int(wishlist_id_)]
 
    itemlist = [] 

    final_list = Items.objects.none()
    print "SHOW SELECTED ITEMS NEW " + str(wishlist_id_)
    for id_ in selected_items_id:
        found_list = original_item_list.filter(id = id_)
        print id_
        print found_list
        final_list = final_list | found_list
        for items in found_list:
            itemlist.append( {"store": str(items.brand), 
                              "category": str(items.cat1), 
                              "price": float(items.price),
                              "sale_price": float(items.saleprice)} )
    selected_items[int(wishlist_id_)] = itemlist
        
    return list_detail.object_list(
                                    request,
                                    queryset = final_list,
                                    template_name = "items_table.html",
                                    extra_context = {'selected_items' : True} )


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
                                           queryset = itemlist,
                                           template_name = "items_table.html"
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

def wishlist2(request): 
    
    if request.method == 'POST':
        
        gender = request.POST.get('gender')
        brand_id = request.POST.get('brands')
        cat_id = request.POST.get('categories')
        
        if len(brand_id) > 0 and cat_id is None:
            form = WishlistForm(request.POST, br_id=brand_id)
        elif len(brand_id) > 0 and cat_id is not None:
            form = WishlistForm(request.POST, br_id=brand_id)
            
            if form.is_valid():
                store = form.cleaned_data['brands']
                item_category = form.cleaned_data['categories']
                gender = form.cleaned_data['gender']
                date = datetime.date.today()
            
                print str(store)
                print str(item_category)
                print str(gender)
                
                try:
                    potential_items = Items.objects.filter(brand__name = store.name)
                    print potential_items
                    # filter only if the category is specified
                    if gender != 'A':
                        potential_items2 = potential_items.filter(gender = gender)
                        print potential_items2
                        potential_items = potential_items2
                        
                    # filter only if category is given
                    potential_items3 = potential_items.filter(cat1__contains = item_category.name)
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
            else:
                print form.errors
                form = WishlistForm(None,br_id=-150)
        else:
            form = WishlistForm(request.POST,br_id=-150)
            print form.errors
            
    else:
        form = WishlistForm(None,br_id=-250)
    
    return render_to_response('wishlist2.html', {'form': form,}, context_instance=RequestContext(request))

def testing_graphs(request):
    pie = Pie([20,30,35]).title('Discounts for sweaters').color('red','lime', 'blue').label('J.Crew', 'Express', 'Banana Republic')
    print pie
    scatter = Scatter([[12,87,75,41],[98,60,27,34],[84,23,69,81]])
    scatter.title('Historical pricing')
    scatter.axes('xy')
    scatter.axes.label(0, 0,20,30,40,)
    scatter.axes.label(1, 0,25,50,75,100)
    scatter.size(300,200)
    
    bar = VerticalBarGroup([[43.56,15.62,78.34], [43.56,15.62,78.34]])
    bar.color('blue', 'red')
    #bar.bar(17,15)
    #bar.size(300,125)
    bar.axes('xy')
    #bar.marker('N*cEUR1*','black',0,-1,11)
    bar.title('Prices at other stores')
    return render_to_response('show_chart.html', {'pie' : pie, 'scatter': scatter, 'bar': bar})

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
            print store
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