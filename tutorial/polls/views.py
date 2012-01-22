# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime, urllib
from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django import forms
from polls.models import Promoinfo, Items, Brands, Categories, ProductModel, CategoryModel, ColorSizeModel, WishlistM, WishlistI
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

### Testing ####
selected_items_id_list[112] = []
######## Visualization Sample Code #############
import gviz_api
from django.db.models import F

####### GLOBALS #######

# Today's date
date_today = None

# All brands (queryset)
br_info = None

# All items for today's date (queryset)
item_info_today = None

# Brand-specific items today (queryset)
br_spec_items_today = []

# Product category-specific items today (queryset)
prod_cat_spec_today = []

# Gender-specific items today (queryset)
gender_spec_today = []

# Combo data (queryset)
combo_item_info = []

# Combo data (numbers)
combo_item_info_stats = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

def stats_update(request):
    global date_today, items_info_today, br_info, prod_cat_info, br_spec_items_today, prod_cat_spec_today, combo_item_info_stats
    
    # Today's date
    date_today = datetime.date.today() # - datetime.timedelta(days=1)
    
    # How many total items available today?
    item_info_today = Items.objects.filter(insert_date__contains=date_today)
    
    # How many brands?
    br_info = Brands.objects.all()
    
    # How many total products available today in each brand?
    br_spec_items_today = []
    for i in range(0, len(br_info)):
        br_spec_items_today.append(item_info_today.filter(brand=br_info[i].id).filter(gender='M'))
        br_spec_items_today.append(item_info_today.filter(brand=br_info[i].id).filter(gender='F'))
    
    #for i in range(0, len(br_spec_items_today)):
    #    print len(br_spec_items_today[i]), len(br_spec_saleitems_today[i])         

    # How many total products available in each category today?
    prod_cat_spec_today = []
    for j in ['jeans', 'shirts', 'skirts', 'sweaters']:
        prod_cat_spec_today.append(item_info_today.filter(cat1__contains=j) | item_info_today.filter(cat2__contains=j) | item_info_today.filter(cat3__contains=j) | item_info_today.filter(cat4__contains=j) | item_info_today.filter(cat5__contains=j))
    
    # How many total products available for each gender today?
    for i in ['M', 'F']:
        gender_spec_today.append(item_info_today.filter(gender=i))
    
    for i in range(0, len(br_info)):
        for j in range(0,len(prod_cat_spec_today)):
            combo_item_info.append(prod_cat_spec_today[j].filter(brand=br_info[i].id).order_by('price'))
            it_avg = combo_item_info[j+i*len(prod_cat_spec_today)].aggregate(Avg('price'))['price__avg']
            it_max = combo_item_info[j+i*len(prod_cat_spec_today)].aggregate(Max('price'))['price__max']
            it_min = combo_item_info[j+i*len(prod_cat_spec_today)].aggregate(Min('price'))['price__min']
            
            it_sp = combo_item_info[j+i*len(prod_cat_spec_today)].filter(saleprice__lt=F('price'))
            if (it_sp):
                it_avg_sp = it_sp.aggregate(Avg('saleprice'))['saleprice__avg']
                it_max_sp = it_sp.filter(saleprice__lt=F('price')).aggregate(Max('saleprice'))['saleprice__max']
                it_min_sp = it_sp.filter(saleprice__lt=F('price')).aggregate(Min('saleprice'))['saleprice__min']
            else:
                it_avg_sp = it_avg
                it_max_sp = it_max
                it_min_sp = it_min
            
            it_median, it_q25, it_q75, it_median_sp, it_q25_sp, it_q75_sp = get_quartiles(combo_item_info[j+i*len(prod_cat_spec_today)], it_sp.order_by('saleprice'))
            it_tnum, it_mnum, it_fnum, it_tnum_sp, it_mnum_sp, it_fnum_sp = get_product_counts(combo_item_info[j+i*len(prod_cat_spec_today)], it_sp)
            combo_item_info_stats[0].append(it_avg)
            combo_item_info_stats[1].append(it_max)
            combo_item_info_stats[2].append(it_min)
            combo_item_info_stats[3].append(it_median)
            combo_item_info_stats[4].append(it_q25)
            combo_item_info_stats[5].append(it_q75)
            combo_item_info_stats[6].append(it_tnum)
            combo_item_info_stats[7].append(it_mnum)
            combo_item_info_stats[8].append(it_fnum)
            combo_item_info_stats[9].append(it_avg_sp)
            combo_item_info_stats[10].append(it_max_sp)
            combo_item_info_stats[11].append(it_min_sp)
            combo_item_info_stats[12].append(it_median_sp)
            combo_item_info_stats[13].append(it_q25_sp)
            combo_item_info_stats[14].append(it_q75_sp)
            combo_item_info_stats[15].append(it_tnum_sp)
            combo_item_info_stats[16].append(it_mnum_sp)
            combo_item_info_stats[17].append(it_fnum_sp)
            
    #print br_info, len(br_spec_items_today), len(prod_cat_spec_today), len(combo_item_info)
    print it_tnum_sp, it_mnum_sp, it_fnum_sp, it_median_sp, it_q25_sp, it_q75_sp 
    return(HttpResponse('Initialized!'))

def get_barplot_jsonstr(data_table, data_arr):    
    
    if (data_arr):
        data = [{"category": "Jeans", "st1": data_arr[0][0], "st2": data_arr[1][0], "st3": data_arr[2][0]},
                {"category": "Shirts", "st1": data_arr[0][1], "st2": data_arr[1][1], "st3": data_arr[2][1]},
                {"category": "Skirts", "st1": data_arr[0][2], "st2": data_arr[1][2], "st3": data_arr[2][2]},
                {"category": "Sweaters", "st1": data_arr[0][3], "st2": data_arr[1][3], "st3": data_arr[2][3]},
                ]
        data_table.LoadData(data)
    else:
        print "Inside get_barplot_jsonstr, empty data_arr", data_arr
        
    return data_table.ToJSon(columns_order=("category", "st1", "st2", "st3"))
    
def get_barplot_gp_jsonstr(data_table, data_arr, gender):    
    
    if (data_arr):
        if ((gender == 'mcnt') or (gender == 'mcnt2')):
            data = [{"category": "Jeans", "st1": data_arr[0][0], "st2": data_arr[1][0], "st3": data_arr[2][0]},
                    {"category": "Shirts", "st1": data_arr[0][1], "st2": data_arr[1][1], "st3": data_arr[2][1]},
                    {"category": "Sweaters", "st1": data_arr[0][3], "st2": data_arr[1][3], "st3": data_arr[2][3]},
                    ]
        elif ((gender == 'fcnt') or (gender == 'fcnt2')):
            data = [{"category": "Jeans", "st1": data_arr[0][0], "st2": data_arr[1][0], "st3": data_arr[2][0]},
                    {"category": "Skirts", "st1": data_arr[0][2], "st2": data_arr[1][2], "st3": data_arr[2][2]},
                    {"category": "Sweaters", "st1": data_arr[0][3], "st2": data_arr[1][3], "st3": data_arr[2][3]},
                    ]
        data_table.LoadData(data)
    else:
        print "Inside get_barplot_gp_jsonstr, empty data_arr", data_arr
        
    return data_table.ToJSon(columns_order=("category", "st1", "st2", "st3"))

def get_barplot_jsonstrs(**kwargs):
    # Describe table
    description = {"category": ("string", "Category"),
                   "st1": ("number", "Express"),
                   "st2": ("number", "J.Crew"),
                   "st3": ("number", "Banana Republic")}
    
    # Load it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    
    # Load data into table
    json_str = {}
    for i in ['cnt', 'avg', 'min', 'max']: 
        json_str[i] = get_barplot_jsonstr(data_table, kwargs[i])
    
    for j in ['mcnt', 'fcnt']:
        json_str[j] = get_barplot_gp_jsonstr(data_table, kwargs[j], j)
    
    return json_str['cnt'], json_str['avg'], json_str['min'], json_str['max'], json_str['mcnt'], json_str['fcnt']

def get_barplot_ival_jsonstr(**kwargs):
    
    avgarr = kwargs['avg']
    minarr = kwargs['min'] 
    maxarr = kwargs['max']
    
    # Describe table
    description = {"category": ("string", "Category"),
                   "st1": ("number", "Express"),
                   "st2": ("number", "", {'type':'number', 'role':'interval'}),
                   "st3": ("number", "", {'type':'number', 'role':'interval'}),
                   "st4": ("number", "J.Crew"),
                   "st5": ("number", "", {'type':'number', 'role':'interval'}),
                   "st6": ("number", "", {'type':'number', 'role':'interval'}),
                   "st7": ("number", "Banana Republic"),
                   "st8": ("number", "", {'type':'number', 'role':'interval'}),
                   "st9": ("number", "", {'type':'number', 'role':'interval'})
                   }
    
    # Load it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    if (avgarr and minarr and maxarr):
        data = [{"category": "Jeans", 
                 "st1": avgarr[0][0], "st2": minarr[0][0], "st3": maxarr[0][0], 
                 "st4": avgarr[1][0], "st5": minarr[1][0], "st6": maxarr[1][0], 
                 "st7": avgarr[2][0], "st8": minarr[2][0], "st9": maxarr[2][0]},
                {"category": "Shirts", 
                 "st1": avgarr[0][1], "st2": minarr[0][1], "st3": maxarr[0][1], 
                 "st4": avgarr[1][1], "st5": minarr[1][1], "st6": maxarr[1][1],
                 "st7": avgarr[2][1], "st8": minarr[2][1], "st9": maxarr[2][1]},
                {"category": "Skirts", 
                 "st1": avgarr[0][2], "st2": minarr[0][2], "st3": maxarr[0][2], 
                 "st4": avgarr[1][2], "st5": minarr[1][2], "st6": maxarr[1][2],
                 "st7": avgarr[2][2], "st8": minarr[2][2], "st9": maxarr[2][2]},
                {"category": "Sweaters", 
                 "st1": avgarr[0][3], "st2": minarr[0][3], "st3": maxarr[0][3], 
                 "st4": avgarr[1][3], "st5": minarr[1][3], "st6": maxarr[1][3],
                 "st7": avgarr[2][3], "st8": minarr[2][3], "st9": maxarr[2][3]},
                ]
        data_table.LoadData(data)
    else:
        print "Inside get_barplot_ival_jsonstr, empty arrs", avgarr, minarr, maxarr
        
    return data_table.ToJSon()
    
def get_cstick_str(idx, min_arr, q25_arr, median_arr, q75_arr, max_arr):
    
    data = [["Jeans", min_arr[idx][0], q25_arr[idx][0], median_arr[idx][0], q75_arr[idx][0], 
             min_arr[idx+1][0], q25_arr[idx+1][0], median_arr[idx+1][0], q75_arr[idx+1][0], 
             min_arr[idx+2][0], q25_arr[idx+2][0], median_arr[idx+2][0], q75_arr[idx+2][0]],
            ["Shirts", min_arr[idx][1], q25_arr[idx][1], median_arr[idx][1], q75_arr[idx][1], 
             min_arr[idx+1][1], q25_arr[idx+1][1], median_arr[idx+1][1], q75_arr[idx+1][1],
             min_arr[idx+2][1], q25_arr[idx+2][1], median_arr[idx+2][1], q75_arr[idx+2][1]],
            ["Skirts", min_arr[idx][2], q25_arr[idx][2], median_arr[idx][2], q75_arr[idx][2], 
             min_arr[idx+1][2], q25_arr[idx+1][2], median_arr[idx+1][2], q75_arr[idx+1][2],
             min_arr[idx+2][2], q25_arr[idx+2][2], median_arr[idx+2][2], q75_arr[idx+2][2]],
            ["Sweaters", min_arr[idx][3], q25_arr[idx][3], median_arr[idx][3], q75_arr[idx][3], 
             min_arr[idx+1][3], q25_arr[idx+1][3], median_arr[idx+1][3], q75_arr[idx+1][3],
             min_arr[idx+2][3], q25_arr[idx+2][3], median_arr[idx+2][3], q75_arr[idx+2][3]],
            ]    
    
    return data
    
def get_cstick_strs(**kwargs):
    data_ret = get_cstick_str(0, kwargs['min'], kwargs['q25'], kwargs['median'], kwargs['q75'], kwargs['max'])
    return data_ret
    
def get_quartiles(it_ob, it_ob2):
    twentyfiveq = len(it_ob)/4
    midpoint = len(it_ob)/2
    seventyfiveq = len(it_ob)/2 + len(it_ob)/4
    if (midpoint % 2):
        median = (it_ob[midpoint].price + it_ob[midpoint+1].price) / 2
        q25 = (it_ob[twentyfiveq].price + it_ob[twentyfiveq+1].price) / 2
        q75 = (it_ob[seventyfiveq].price + it_ob[seventyfiveq+1].price) / 2
    else:
        median = it_ob[midpoint].price
        q25 = it_ob[twentyfiveq].price
        q75 = it_ob[seventyfiveq].price
        
    if (it_ob2):
        twentyfiveq = len(it_ob2)/4
        midpoint = len(it_ob2)/2
        seventyfiveq = len(it_ob2)/2 + len(it_ob2)/4
        if (midpoint % 2):
            median_sp = (it_ob2[midpoint].price + it_ob2[midpoint+1].price) / 2
            q25_sp = (it_ob2[twentyfiveq].price + it_ob2[twentyfiveq+1].price) / 2
            q75_sp = (it_ob2[seventyfiveq].price + it_ob2[seventyfiveq+1].price) / 2
        else:
            median_sp = it_ob2[midpoint].price
            q25_sp = it_ob2[twentyfiveq].price
            q75_sp = it_ob2[seventyfiveq].price
    else:
        median_sp = median
        q25_sp = q25
        q75_sp = q75
    
    return median, q25, q75, median_sp, q25_sp, q75_sp

def get_product_counts(it, it_sp):
    
    total_cnt = it.aggregate(Count('price'))['price__count']
    men_cnt = it.filter(gender='M').aggregate(Count('price'))['price__count']
    women_cnt = it.filter(gender='F').aggregate(Count('price'))['price__count']
    
    if (it_sp):
        total_cnt_sp = it_sp.aggregate(Count('price'))['price__count']
        men_cnt_sp = it_sp.filter(gender='M').aggregate(Count('price'))['price__count']
        women_cnt_sp = it_sp.filter(gender='F').aggregate(Count('price'))['price__count']
    else:
        total_cnt_sp = 0
        men_cnt_sp = 0
        women_cnt_sp = 0
           
    return total_cnt, men_cnt, women_cnt, total_cnt_sp, men_cnt_sp, women_cnt_sp
    
def stats_plot(request):
        
    avgarr = []
    minarr = []
    maxarr = []
    medianarr = []
    q25arr = []
    q75arr = []
    cntarr = []
    mcntarr = []
    fcntarr = []
    
    avgnumarr = []
    minnumarr = []
    maxnumarr = []
    cntnumarr = [[],[],[]]
    mediannumarr = []
    q25numarr = []
    q75numarr = []

    avgarr_sp = []
    minarr_sp = []
    maxarr_sp = []
    medianarr_sp = []
    q25arr_sp = []
    q75arr_sp = []
    cntarr_sp = []
    mcntarr_sp = []
    fcntarr_sp = []
    
    avgnumarr_sp = []
    minnumarr_sp = []
    maxnumarr_sp = []
    cntnumarr_sp = [[],[],[]]
    mediannumarr_sp = []
    q25numarr_sp = []
    q75numarr_sp = []
    
    for i in range(0,len(combo_item_info)+1):
        
        if ((i > 0) and ((i % len(prod_cat_spec_today)) == 0)):
            avgarr.append(avgnumarr)
            minarr.append(minnumarr)
            maxarr.append(maxnumarr)
            medianarr.append(mediannumarr)
            q25arr.append(q25numarr)
            q75arr.append(q75numarr)
            cntarr.append(cntnumarr[0])
            mcntarr.append(cntnumarr[1])
            fcntarr.append(cntnumarr[2])
            
            avgarr_sp.append(avgnumarr_sp)
            minarr_sp.append(minnumarr_sp)
            maxarr_sp.append(maxnumarr_sp)
            medianarr_sp.append(mediannumarr_sp)
            q25arr_sp.append(q25numarr_sp)
            q75arr_sp.append(q75numarr_sp)
            cntarr_sp.append(cntnumarr_sp[0])
            mcntarr_sp.append(cntnumarr_sp[1])
            fcntarr_sp.append(cntnumarr_sp[2])
     
            avgnumarr = []
            minnumarr = []
            maxnumarr = []
            cntnumarr = [[],[],[]]
            mediannumarr = []
            q25numarr = []
            q75numarr = []
            
            avgnumarr_sp = []
            minnumarr_sp = []
            maxnumarr_sp = []
            cntnumarr_sp = [[],[],[]]
            mediannumarr_sp = []
            q25numarr_sp = []
            q75numarr_sp = []
            
            if (i == len(combo_item_info)):
                break
                
        avgnumarr.append(combo_item_info_stats[0][i])
        maxnumarr.append(combo_item_info_stats[1][i])
        minnumarr.append(combo_item_info_stats[2][i])
        mediannumarr.append(combo_item_info_stats[3][i])
        q25numarr.append(combo_item_info_stats[4][i])
        q75numarr.append(combo_item_info_stats[5][i]) 
        cntnumarr[0].append(combo_item_info_stats[6][i])
        cntnumarr[1].append(combo_item_info_stats[7][i])
        cntnumarr[2].append(combo_item_info_stats[8][i])
        
        avgnumarr_sp.append(combo_item_info_stats[9][i])
        maxnumarr_sp.append(combo_item_info_stats[10][i])
        minnumarr_sp.append(combo_item_info_stats[11][i])
        mediannumarr_sp.append(combo_item_info_stats[12][i])
        q25numarr_sp.append(combo_item_info_stats[13][i])
        q75numarr_sp.append(combo_item_info_stats[14][i]) 
        cntnumarr_sp[0].append(combo_item_info_stats[15][i])
        cntnumarr_sp[1].append(combo_item_info_stats[16][i])
        cntnumarr_sp[2].append(combo_item_info_stats[17][i])
    #print "C: ", datetime.datetime.now()

    #print avgarr, minarr, maxarr
    
    #print len(medianarr), len(avgarr)
    
    json1, json2, json3, json4, json8, json9 = get_barplot_jsonstrs(cnt=cntarr, avg=avgarr, min=minarr, max=maxarr, mcnt=mcntarr, fcnt=fcntarr)
    json5 = get_cstick_strs(min=minarr, median=medianarr, q25=q25arr, q75=q75arr, max=maxarr)
    json6 = get_barplot_ival_jsonstr(avg=avgarr, min=minarr, max=maxarr)
    json7 = get_barplot_ival_jsonstr(avg=medianarr, min=minarr, max=q75arr)
    
    json10, json11, json12, json13, json14, json15 = get_barplot_jsonstrs(cnt=cntarr_sp, avg=avgarr_sp, min=minarr_sp, max=maxarr_sp, mcnt=mcntarr_sp, fcnt=fcntarr_sp)
    json16 = get_cstick_strs(min=minarr_sp, median=medianarr_sp, q25=q25arr_sp, q75=q75arr_sp, max=maxarr_sp)
    #json6 = get_barplot_ival_jsonstr(avg=avgarr, min=minarr, max=maxarr)
    json17 = get_barplot_ival_jsonstr(avg=medianarr_sp, min=minarr_sp, max=q75arr_sp)
    
    return render_to_response('gviz-test.html', {'json1': json1, 
                                                 'json2': json2, 
                                                 'json3': json3, 
                                                 'json4': json4, 
                                                 'json5': json5,  
                                                 'json6': json6,
                                                 'json7': json7,
                                                 'json8': json8, 
                                                 'json9': json9,
                                                 'json11': json11,
                                                 'json12': json12,
                                                 'json13': json13,
                                                 'json14': json14,
                                                 'json15': json15,
                                                 'json16': json16, 
                                                 'json17': json17,}) 



######## End Visualization Sample Code #############


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

def old_wishlist_table(prod_arr):
    wishlist_id_ = 112
    # Multiple entries can be returned as we can have duplicates in the database right now
    print "Adding item " + str(prod_arr[0].idx) + " to wishlist id " + str(wishlist_id_)
    selected_items_id_list[int(wishlist_id_)].append(prod_arr[0].idx)
    print selected_items_id_list[int(wishlist_id_)]
    selected_items[int(wishlist_id_)] = []
    # From show_selected_items_new
    itemlist = []
    final_list = ProductModel.objects.none()
    selected_items_id = selected_items_id_list[int(wishlist_id_)]
    for id_ in selected_items_id:
        found_list = ProductModel.objects.filter(idx = id_)
        print id_, found_list
        final_list = final_list | found_list
        for items in found_list:
            itemlist.append( {"store": str(items.brand), 
                              "category": str(items.name), 
                              "price": float(items.price),
                              "sale_price": float(items.saleprice)} )
    selected_items[int(wishlist_id_)] = itemlist    
    return final_list, selected_items

def insert_product_in_wishlist_new(userid, matched_prod_obj):
    # Check if item already in database
    w = WishlistI.objects.filter(user_id=userid).filter(item=matched_prod_obj)
    if not w:
        w = WishlistI()
        w.user_id = userid
        w.item = matched_prod_obj
        w.save()
        resp = "Added Item to Wishlist!"
    else:
        resp = "Item already in Wishlist!"
    return w, resp

def shelfit(request, d1, d2):
    
    #print d1, d2
    
    if 'u' in request.GET and request.GET['u'] and 't' in request.GET and request.GET['t']:
        
        # Get User ID
        userid = urllib.unquote(request.GET['t'].decode('utf-8'))
        
        # Get product URL
        prod_url = urllib.unquote(request.GET['u'].decode('utf-8')) 
        
        # Get item ID and brand name
        spl1 = prod_url.split("/")
        brand_name = spl1[2].split(".")[1]
        prod_id = -111
        prod_info = []
        for i in range(3, len(spl1)):
            if (brand_name == "express"): 
                prod_info = spl1[i].split("-")
            elif (brand_name == "jcrew"):
                prod_info = spl1[i].split("~")
            print prod_info
            for i in prod_info:
                try:
                    prod_id = int(i)
                except ValueError:
                    pass
                else:
                    break
            if (prod_id > 0):
                break
    
        if (((brand_name == "express") or (brand_name == "jcrew")) and 
            (prod_id > 0)):
            
            # Find product in database
            prod_arr = ProductModel.objects.filter(idx=prod_id)
            
            print userid, prod_arr[0].idx
            
            # Add product to wishlist
            w, resp = insert_product_in_wishlist_new(userid, prod_arr[0])
        
            # From show_selected_items_new
            wishlist_id_ = 112
            selected_items[int(wishlist_id_)] = []
            itemlist = []
            final_list = WishlistI.objects.filter(item=prod_arr[0])
            for wi in final_list:
                catlist = CategoryModel.objects.filter(product=wi)
                if catlist:
                    itemlist.append( {"store": str(wi.item.brand), 
                                      "category": str(catlist[0].categoryName), 
                                      "name": str(wi.item.name),
                                      "price": float(wi.item.price),
                                      "sale_price": float(wi.item.saleprice)} )
                else:
                    itemlist.append( {"store": str(wi.item.brand), 
                                      "category": "None", 
                                      "name": str(wi.item.name),
                                      "price": float(wi.item.price),
                                      "sale_price": float(wi.item.saleprice)} )
            
            selected_items[int(wishlist_id_)] = itemlist
            return list_detail.object_list(request,
                                           queryset = final_list,
                                           template_name = "items_table2.html",
                                           extra_context = {'selected_items' : True, 'curresp' : resp, 'num_selected' : len(final_list), 'uid': userid} )
        else:
            if not ((brand_name == "express") or (brand_name == "jcrew")):
                return HttpResponse('<p>Please choose products from <a href="http://www.express.com/"/>express.com</a> or <a href="http://www.jcrew.com/"/>jcrew.com</a>.</p><p>We are in the process of adding more stores.</p><p><strong>Thank you for bearing with us (in the meanwhile). We really appreciate your patronage!</strong></p>')
            else:
                return HttpResponse('<p>Please choose products from a valid product page (from <a href="http://www.express.com/"/>express.com</a> or <a href="http://www.jcrew.com/"/>jcrew.com</a>).</p><p>We are in the process of adding more stores.</p><p><strong>Thank you for bearing with us (in the meanwhile). We really appreciate your patronage!</strong></p>')
    else:
        return HttpResponse('Please use ShelfIt from a filled-in product page!')

def yourshelf_detail(request, d1, d2):
    
    if 'u' in request.GET and request.GET['u'] and (('s' in request.GET and request.GET['s']) or ('c' in request.GET and request.GET['c'])):
        
        # Get User ID
        userid = urllib.unquote(request.GET['u'].decode('utf-8'))
        
        # Brand-specific info request
        if ('s' in request.GET and request.GET['s']):
            brand_name = urllib.unquote(request.GET['s'].decode('utf-8'))
            
            selected_items[int(userid)] = []
            itemlist = []
            final_list = WishlistI.objects.filter(user_id=userid)
            br_list = WishlistI.objects.none()
            for wi in final_list:
                if wi.item.brand.name == brand_name:
                    br_list = br_list | WishlistI.objects.filter(item=wi.item)
                    catlist = CategoryModel.objects.filter(product=wi.item)
                    #print catlist
                    if catlist:
                        itemlist.append( {"store": str(wi.item.brand), 
                                          "category": str(catlist[0].categoryName), 
                                          "name": str(wi.item.name),
                                          "price": float(wi.item.price),
                                          "sale_price": float(wi.item.saleprice)} )
                    else:
                        itemlist.append( {"store": str(wi.item.brand), 
                                          "category": "None", 
                                          "name": str(wi.item.name),
                                          "price": float(wi.item.price),
                                          "sale_price": float(wi.item.saleprice)} )
            
            selected_items[int(userid)] = itemlist
            return list_detail.object_list(request,
                                           queryset = br_list,
                                           template_name = "items_table2.html",
                                           extra_context = {'selected_items' : True, 'num_selected' : len(br_list), 'uid': userid} )
        
        elif ('c' in request.GET and request.GET['c']):
            # Category-specific request
            cat_name = urllib.unquote(request.GET['c'].decode('utf-8'))
            qs_arr = items_per_cat[userid]
            #print cat_name, qs_arr
    
            return list_detail.object_list(request,
                                           queryset = qs_arr[cat_name],
                                           template_name = "items_table2.html",
                                           extra_context = {'selected_items' : True, 'num_selected' : len(qs_arr[cat_name]), 'uid': userid} )
            
    else:
        return HttpResponse('Dear user: please login or create an account before accessing this page...')

def yourshelf_concise(request, d1, d2):

    if 'u' in request.GET and request.GET['u']:
        # Get User ID
        userid = urllib.unquote(request.GET['u'].decode('utf-8'))
        
        # Get Info brand-wise
        selected_items[int(userid)] = []
        itemlist = []
        final_list = WishlistI.objects.filter(user_id=userid)
        br_list1 = WishlistI.objects.none()
        br_list2 = WishlistI.objects.none()
        k=0
        for wi in final_list:
            k += 1
            #print wi
            catlist = CategoryModel.objects.filter(product=wi.item)
            #print catlist
            if catlist:
                itemlist.append( {"store": str(wi.item.brand), 
                                  "category": str(catlist[0].categoryName), 
                                  "name": str(wi.item.name),
                                  "price": float(wi.item.price),
                                  "sale_price": float(wi.item.saleprice)} )
            else:
                itemlist.append( {"store": str(wi.item.brand), 
                                  "category": "None", 
                                  "name": str(wi.item.name),
                                  "price": float(wi.item.price),
                                  "sale_price": float(wi.item.saleprice)} )
            
            if wi.item.brand.name == "Express":
                tmpqset = WishlistI.objects.filter(item=wi.item)
                if len(tmpqset) > 1: 
                    br_list1 = br_list1 | tmpqset[0]
                else:
                    br_list1 = br_list1 | tmpqset
            if wi.item.brand.name == "J.Crew":
                tmpqset = WishlistI.objects.filter(item=wi.item)
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
               qs_arr[i] = qs_arr[i] | WishlistI.objects.filter(item=j)
    
        #print qs_arr
        items_per_cat[userid] = qs_arr
        
        html = '<p><strong>Categorization By Store</strong></p>'
        html += '<table border=1><tr><th>Express</th><th>J.Crew</th><tr><td><a href=detail/?u=' + str(userid) + '&s=' + 'Express>'
        html += str(len(br_list1)) + ' Items</a></td><td>' 
        html += '<a href=detail/?u=' + str(userid) + '&s=' + 'J.Crew>'
        html += str(len(br_list2)) + ' Items</a></td></tr></table>'
        
        html += '<p><strong>Categorization By Item Type</strong></p>'
        html += '<table border=1><tr>'
        for i in catlist:
            if i == 'Dress':
                html += '<th>' + str(i) + 'es</th>'
            else:
                html += '<th>' + str(i) + 's</th>'
                
        html += '<tr>'
        for i in catlist:
            html += '<td><a href=detail/?u=' + str(userid) + '&c=' + str(i) + '>'
            html += str(len(qs_arr[i])) + ' Items</a></td>'
        html += '</tr></table>'
        
        return HttpResponse(html)
    
    else:
        return HttpResponse('Dear user: please login or create an account before accessing this page...')
        
'''
    This function should return a html page dynamically generated 
    after seeing the number of existing users and adding to them
    If same person uses this multiple times, we have currently no way 
    of knowing...need support for sessions, users and registration. 
'''
def add_shelfit_bmarklet(request):
    
    # Get existing user IDs
    w_qs = WishlistI.objects.values('user_id').distinct()
    len_qs = len(w_qs)
    last_uid = w_qs[len_qs-1]['user_id']
    
    html = '<p>Please copy the code below, open your Bookmarks manager, create new bookmark, type' 
    html += ' <strong>Shelf It!</strong> into the name field and paste the code into the URL field.</p>'
    html += '<textarea rows="5" cols="120" readonly="readonly">'
    html += 'javascript:var d=document,w=window,e=w.getSelection,k=d.getSelection,x=d.selection,'
    html += 's=(e?e():(k)?k():(x?x.createRange().text:0)),f=\'http://shopelfify.com:8000/shelfit\',l=d.location'
    html += ',e=encodeURIComponent,u=f+\'?u=\'+e(l.href)+\'&t=' + str(last_uid+1) + '\';'
    html += 'a=function(){if(!w.open(u,\'t\',\'toolbar=0,resizable=1,scrollbars=1,status=1,width=720,height=570\'))l.href=u;};'
    html += 'if (/Firefox/.test(navigator.userAgent)) setTimeout(a, 0); else a();void(0)</textarea>'
    
    #print html
    
    return HttpResponse(html)

def apply_discount_new(request, d1):
    
    if 'u' in request.GET and request.GET['u']:
        
        # Get User ID
        userid = urllib.unquote(request.GET['u'].decode('utf-8'))
        
        item_list = selected_items[int(userid)]
        
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
        html = "<html><body><p>Store 1: Total cost: $" + str(orig_cost) + ". With promotion: $" + str(total_cost) + " We saved $" + \
            str(savings) + " Free shipping?" + str(shipping) + "</p>" 
        print html
        
        promo_store = promo_date.filter(store = 2)
        promo = promo_store
        orig_cost, total_cost, savings, shipping = match.match(store_name, date_, copy.deepcopy(item_list), promo)
        html += "<p>Store 2: Total cost: $" + str(orig_cost) + ". With promotion: $" + str(total_cost) + " We saved $" + \
            str(savings) + " Free shipping?" + str(shipping) + "</p>" 
        print html
    
        promo_store = promo_date.filter(store = 3)    
        promo = promo_store
        orig_cost, total_cost, savings, shipping = match.match(store_name, date_, copy.deepcopy(item_list), promo)
        html += "<p>Store 3: Total cost: $" + str(orig_cost) + ". With promotion: $" + str(total_cost) + " We saved $" + \
            str(savings) + " Free shipping?" + str(shipping) + "</p></body></html>" 
        print html    
        
        return HttpResponse(html)
    else:
        return HttpResponse('Dear user: please login or create an account before accessing this page...')


##### End ShelfIt #################

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
    
def home(request):
     return render_to_response('home.html', {'uid':1})    

def create_wishlist(request):
    return render_to_response('create_wishlist.html')



def view_promo(request):
    return render_to_response('view_promo.html')
    
def add_item_to_selected_items_list(request, wishlist_id_, item_id_, page_id_):
    print "Adding item " + str(item_id_) + " to wishlist id " + str(wishlist_id_)
    selected_items_id_list[int(wishlist_id_)].append(item_id_)
    selected_items[int(wishlist_id_)] = []
    print selected_items_id_list[int(wishlist_id_)]
    print page_id_
    return HttpResponseRedirect("/wishlist/" + wishlist_id_ + "/?page=" + str(page_id_))

def compare_promo(request):
    promos = Promoinfo.objects.filter(d = datetime.date(2012, 1, 7)).filter(store = 1)
    print promos
    coupon = match._fill_coupon_dbinfo(promos, "Express")
    #match.print_coupon(coupon)
    p = promotion.create_new_promo(promos, "Express")
    print "Printing promotions:\n" + str(p)
    
    
def draw_plot1(chart_max, a1, a2, a3, a4):
    #bar = VerticalBarGroup([avgnum['jeans'],
    #                        avgnum['shirts'], 
    #                        avgnum['skirts'],
    #                        avgnum['sweaters']], 
    #                       encoding='text') 
    bar = VerticalBarGroup([a1, a2, a3, a4], 
                            encoding='text')
    bar.color('0000FF55', 'FF000055', '00FF0055', 'orange')
    bar.axes('xy')
    bar.title('Average Price (USD) Comparison')
    bar.scale(0,chart_max+10)
    #bar.bar(17,15)
    bar.size(500,200)
    #bar.size(200,100)
    #bar.axes('xy')
    bar.axes.label(0, 'Express', 'JCrew', 'Banana Republic')
    bar.axes.label(1, None, '20', '40', '60', '80', '100', '120', '140', '160', '180', '200', '220')
    #bar.axes.label(1, 'Average Price (USD)')
    bar.legend('Jeans', 'Shirts', 'Skirts', 'Sweaters')
    #bar.marker('N*cEUR1*','black',0,-1,11)
    bar.axes.range(1, 0.0,chart_max+10)
    #bar.title('Price comparison across stores','00cc00',12)
    
    return bar

def draw_plot2(chart_max2, a1, a2, a3):
    bar2 = VerticalBarGroup([a1, a2, a3], 
                             encoding='text') 
    bar2.color('0000FF55', 'FF000055', '00FF0055')
    bar2.axes('xy')
    bar2.bar(20,1,15)
    bar2.title('Average Price (USD) Comparison')
    bar2.scale(0,chart_max2+10)
    bar2.size(500,200)
    bar2.axes.label(0, 'Jeans', 'Shirts', 'Skirts', 'Sweaters')
    bar2.axes.label(1, None, '20', '40', '60', '80', '100', '120', '140', '160', '180', '200', '220')
    bar2.legend('Express', 'J.Crew', 'Banana Republic')
    #bar.marker('N*cEUR1*','black',0,-1,11)
    bar2.axes.range(1, 0.0,chart_max2+10)
    
    return bar2
    
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
    
    #===========================================================================
    # avgnum = {}
    # chart_max = 0
    # for i in ['shirts', 'jeans', 'skirts', 'sweaters']: # Get this as input from User?
    #    avgnumarr = []
    #    minnumarr = []
    #    maxnumarr = []
    #    for j in range(0,len(br_info)):
    #        # Currently, we only get items that match cat1. What about others?
    #        it1 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[j].id).filter(cat1__contains=i)
    #        it2 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[j].id).filter(cat2__contains=i)
    #        it3 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[j].id).filter(cat3__contains=i)
    #        it4 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[j].id).filter(cat4__contains=i)
    #        it5 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[j].id).filter(cat5__contains=i)
    #        
    #        # Find unique products that include i in any of cat1 to cat5
    #        it = it1 | it2 | it3 | it4 | it5
    #        
    #        it_max = it.aggregate(Max('price'))['price__max']
    #        it_min = it.aggregate(Min('price'))['price__min']
    #        it_avg = it.aggregate(Avg('price'))['price__avg']
    #        it_num = it.aggregate(Count('price'))['price__count']
    #        print date_today, br_info[j].name, i, it_num, it_min, it_avg, it_max
    #        avgnumarr.append(it_avg)
    #        minnumarr.append(it_min)
    #        maxnumarr.append(it_max)
    #        if it_avg > chart_max:
    #            chart_max = it_avg
    #    avgnum[i] = avgnumarr
    #    minnum[i] = minnumarr
    #    maxnum[i] = maxnumarr
    #===========================================================================
        
    #print avgnum
    
    #bar1 = draw_plot1(chart_max, avgnum['jeans'], avgnum['shirts'], avgnum['skirts'], avgnum['sweaters'])
    
    avgnum2 = []
    minnum2 = []
    maxnum2 = []
    chart_avgmax2 = 0
    for i in range(0,len(br_info)):
        avgnum2arr = []
        minnum2arr = []
        maxnum2arr = []
        for j in ['shirts', 'jeans', 'skirts', 'sweaters']: # Get this as input from User?
            # Currently, we only get items that match cat1. What about others?
            it1 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[i].id).filter(cat1__contains=j)
            it2 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[i].id).filter(cat2__contains=j)
            it3 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[i].id).filter(cat3__contains=j)
            it4 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[i].id).filter(cat4__contains=j)
            it5 = Items.objects.filter(insert_date__contains=date_today).filter(brand=br_info[i].id).filter(cat5__contains=j)
            
            # Find unique products that include i in any of cat1 to cat5
            it = it1 | it2 | it3 | it4 | it5
            
            it_max = it.aggregate(Max('price'))['price__max']
            it_min = it.aggregate(Min('price'))['price__min']
            it_avg = it.aggregate(Avg('price'))['price__avg']
            it_num = it.aggregate(Count('price'))['price__count']
            print date_today, br_info[i].name, j, it_num, it_min, it_avg, it_max
            avgnum2arr.append(it_avg)
            minnum2arr.append(it_min)
            maxnum2arr.append(it_max)
            if it_avg > chart_avgmax2:
                chart_avgmax2 = it_avg
        
        avgnum2.append(avgnum2arr)
        minnum2.append(minnum2arr)
        maxnum2.append(maxnum2arr)
        
    print avgnum2
    #print avgnum2[0][0], avgnum2[0][1], avgnum2[0][2], avgnum2[0][3] 
    
    bar2 = draw_plot2(chart_avgmax2, avgnum2[0], avgnum2[1], avgnum2[2])
    
    #===========================================================================
    # avgnum3 = [10, avgnum2[0][0], avgnum2[0][1], avgnum2[0][2], avgnum2[0][3], 10]
    # minnum3 = [10, minnum2[0][0], minnum2[0][1], minnum2[0][2], minnum2[0][3], 10]
    # maxnum3 = [10, maxnum2[0][0], maxnum2[0][1], maxnum2[0][2], maxnum2[0][3], 10]
    # 
    # print avgnum2[0]
    # 
    # line = Line([[0,0,0,0,0],
    #             minnum3,
    #             avgnum3,
    #             avgnum3,
    #             maxnum3],
    #            encoding='text',series=1)
    # #line.scale(0,100,-50,100)
    # line.scale(0,100)
    # line.marker('F','',1,'1:4',20)
    # line.axes('xy')
    # line.axes.range(0, 0,100)
    # line.axes.range(1, 0,100)
    # line.axes.label(0, None, 'Jeans', 'Shirts', 'Skirts', 'Sweaters', None)
    # line.title('Price Comparison (USD)')
    #===========================================================================
    
    #bar.title('Price comparison across stores','00cc00',12)
    return render_to_response('show_pricecomp.html', {'bar': bar2}) #{'pie' : pie, 'scatter': scatter, 'bar': bar})
    
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