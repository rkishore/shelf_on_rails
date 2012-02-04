import gviz_api, datetime
from django.db.models import F
from django.http import HttpResponse #, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from debra.models import Brands, Items, SSItemStats, UserIdMap
from django.db.models import Avg, Max, Min, Count

''' The following functions plot data in a format that can be used 
    by the google visualization javascript API
'''
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
        try: 
            json_str[i] = get_barplot_jsonstr(data_table, kwargs[i])
        except KeyError:
            pass
        
    for j in ['mcnt', 'fcnt']:
        try:
            json_str[j] = get_barplot_gp_jsonstr(data_table, kwargs[j], j)
        except KeyError:
            pass
    #return json_str['cnt'], json_str['avg'], json_str['min'], json_str['max'], json_str['mcnt'], json_str['fcnt']
    return json_str

def get_barplot_ival_jsonstr(**kwargs):
    
    avgarr = kwargs['avg']
    minarr = kwargs['min'] 
    maxarr = kwargs['max']
    gender = kwargs['gender']
    
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
        if (gender == 'A'):
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
        elif (gender == 'M'):
            data = [{"category": "Jeans", 
                     "st1": avgarr[0][0], "st2": minarr[0][0], "st3": maxarr[0][0], 
                     "st4": avgarr[1][0], "st5": minarr[1][0], "st6": maxarr[1][0], 
                     "st7": avgarr[2][0], "st8": minarr[2][0], "st9": maxarr[2][0]},
                    {"category": "Shirts", 
                     "st1": avgarr[0][1], "st2": minarr[0][1], "st3": maxarr[0][1], 
                     "st4": avgarr[1][1], "st5": minarr[1][1], "st6": maxarr[1][1],
                     "st7": avgarr[2][1], "st8": minarr[2][1], "st9": maxarr[2][1]},
                    {"category": "Sweaters", 
                     "st1": avgarr[0][3], "st2": minarr[0][3], "st3": maxarr[0][3], 
                     "st4": avgarr[1][3], "st5": minarr[1][3], "st6": maxarr[1][3],
                     "st7": avgarr[2][3], "st8": minarr[2][3], "st9": maxarr[2][3]},
                    ]
        elif (gender == 'F'):
            data = [{"category": "Jeans", 
                     "st1": avgarr[0][0], "st2": minarr[0][0], "st3": maxarr[0][0], 
                     "st4": avgarr[1][0], "st5": minarr[1][0], "st6": maxarr[1][0], 
                     "st7": avgarr[2][0], "st8": minarr[2][0], "st9": maxarr[2][0]},
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

'''
    Helper functions to get price statistics (median, quartiles, min, max, ...)
'''
def get_price_quartiles_ss(price_qs, saleprice_qs, statnum):
    
    twentyfiveq = len(price_qs)/4
    seventyfiveq = len(price_qs)/2 + len(price_qs)/4
    midpoint = len(price_qs)/2
    
    midpoint_sale = len(saleprice_qs)/2
    twentyfiveq_sale = len(saleprice_qs)/4
    seventyfiveq_sale = midpoint_sale + twentyfiveq_sale
    
    if statnum == 3:
        if (midpoint % 2):
            price = (price_qs[midpoint].price + price_qs[midpoint+1].price) / 2
        else:
            price = price_qs[midpoint].price
            
        if (saleprice_qs) and len(saleprice_qs) >= 4:
            if (midpoint_sale % 2):
                saleprice = (saleprice_qs[midpoint_sale].saleprice + saleprice_qs[midpoint_sale+1].saleprice) / 2
            else:
                saleprice = saleprice_qs[midpoint_sale].saleprice
        else:
            saleprice = price
    
    elif statnum == 4:
        if (midpoint % 2):
            price = (price_qs[seventyfiveq].price + price_qs[seventyfiveq+1].price) / 2
        else:
            price = price_qs[seventyfiveq].price
        
        if (saleprice_qs) and len(saleprice_qs) >= 4:
            if (midpoint_sale % 2):
                saleprice = (saleprice_qs[seventyfiveq_sale].saleprice + saleprice_qs[seventyfiveq_sale+1].saleprice) / 2
            else:
                saleprice = saleprice_qs[seventyfiveq_sale].saleprice
        else:
            saleprice = price
    
    elif statnum == 5:
        if (midpoint % 2):
            price = (price_qs[twentyfiveq].price + price_qs[twentyfiveq+1].price) / 2
        else:
            price = price_qs[twentyfiveq].price
        
        if (saleprice_qs) and len(saleprice_qs) >= 4:
            if (midpoint_sale % 2):
                saleprice = (saleprice_qs[twentyfiveq_sale].saleprice + saleprice_qs[twentyfiveq_sale+1].saleprice) / 2
            else:
                saleprice = saleprice_qs[twentyfiveq_sale].saleprice
        else:
            saleprice = price
    
    return price, saleprice

def get_price_stats_ss(price_qs, saleprice_qs, statnum):
    
    if not price_qs:
        price, saleprice = -111.0, -111.0
    else:
        if statnum == 0:
            price = price_qs.aggregate(Avg('price'))['price__avg']
            if saleprice_qs:
                saleprice = saleprice_qs.aggregate(Avg('saleprice'))['saleprice__avg']
            else:
                saleprice = price
        elif statnum == 1:
            price = price_qs.aggregate(Max('price'))['price__max']
            if saleprice_qs:
                saleprice = saleprice_qs.aggregate(Max('saleprice'))['saleprice__max']
            else:
                saleprice = price
        elif statnum == 2:
            price = price_qs.aggregate(Min('price'))['price__min']
            if saleprice_qs:
                saleprice = saleprice_qs.aggregate(Min('saleprice'))['saleprice__min']
            else:
                saleprice = price
        elif statnum > 2:
            price, saleprice = get_price_quartiles_ss(price_qs, saleprice_qs, statnum)
    
    return price, saleprice

''' 
    Call to allow database to be populated with today's shopstyle data. 
    SECURITY: Should not be client-facing!
'''
def update_db(request):
    
    date_today = datetime.date.today()
    s = SSItemStats.objects.filter(tdate=date_today)
    if not s:
        item_info_today = Items.objects.filter(insert_date__contains=date_today)
        br_info = Brands.objects.all()         
        prod_cat_spec_today = {}
        for j in ['jeans', 'shirts', 'skirts', 'sweaters']:
            prod_cat_spec_today[j] = item_info_today.filter(cat1__contains=j) | item_info_today.filter(cat2__contains=j) | item_info_today.filter(cat3__contains=j) | item_info_today.filter(cat4__contains=j) | item_info_today.filter(cat5__contains=j)

        for i in range(0, len(br_info)):
            for j in ['jeans', 'shirts', 'skirts', 'sweaters']:
                for k in ['M', 'F']:
                    price_qs = prod_cat_spec_today[j].filter(brand=br_info[i].id).filter(gender=k).order_by('price')
                    tmp_saleprice_qs = price_qs.filter(saleprice__lt=F('price'))
                    if (tmp_saleprice_qs):
                        saleprice_qs = tmp_saleprice_qs.order_by('saleprice')
                    else:
                        saleprice_qs = {}
                    for l in range(0,6): # Price selection metric (0, 'AVERAGE'), (1, 'MAXIMUM'), (2, 'MINIMUM'), (3, 'MEDIAN'), (4, 'Q75'), (5, 'Q25')
                        s = SSItemStats()
                        s.tdate = date_today
                        s.brand = br_info[i]
                        s.category = j
                        s.gender = k
                        s.price_selection_metric = l
                        s.total_cnt = price_qs.aggregate(Count('price'))['price__count']
                        if saleprice_qs:
                            s.sale_cnt = saleprice_qs.aggregate(Count('price'))['price__count']
                        else:
                            s.sale_cnt = 0
                        s.price, s.saleprice = get_price_stats_ss(price_qs, saleprice_qs, l)
                        s.save()
                        
        resp = 'Initialized!'
    else:
        resp = 'Already Initialized!'
                                
    return(HttpResponse(resp))

'''
    Call to plot statistics from today's shopstyle data. 
'''
def plot_from_db(request):
    
    try:
        ipaddr_csv = request.META['REMOTE_ADDR']    
    except KeyError:
        ipaddr = 'unknown'       
        return HttpResponse('<p>Oops - your elf has gone shopping! Please try again later while we ask her to get back to work.</p>')
    else:
        print ipaddr_csv
        ipaddr = ipaddr_csv.split(',')[0]
        uid_obj = UserIdMap.objects.filter(ip_addr=ipaddr)
        print uid_obj
        if (uid_obj):
            userid = uid_obj[0].user_id

    print userid

    price_select_metrics = {'average': 0, 'max': 1, 'min': 2, 'median': 3, 'q75': 4, 'q25': 5}
    
    br_info = Brands.objects.all()
    
    # Items on sale for men, women
    w_perc_arr = []
    m_perc_arr = []
    w_median_arr = []
    m_median_arr = []
    w_min_arr = []
    m_min_arr = []
    w_q75_arr = []
    m_q75_arr = []
    for i in range(0, len(br_info)):
        w_perc_arr.append([])
        m_perc_arr.append([])
        w_median_arr.append([])
        m_median_arr.append([])
        w_min_arr.append([])
        m_min_arr.append([])
        w_q75_arr.append([])
        m_q75_arr.append([])
        
        for j in ['jeans', 'shirts', 'skirts', 'sweaters']: 
            tmp = SSItemStats.objects.filter(brand=br_info[i].id).filter(category=j)
            tmp_w = tmp.filter(gender='F')
            tmp_m = tmp.filter(gender='M')
            if (tmp_w[0].total_cnt):
                perc_sale_w = (tmp_w[0].sale_cnt * 100) / (tmp_w[0].total_cnt)
            else:
                perc_sale_w = 0
            if (tmp_m[0].total_cnt):
                perc_sale_m = (tmp_m[0].sale_cnt * 100) / (tmp_m[0].total_cnt)
            else:
                perc_sale_m = 0
            w_perc_arr[i].append(perc_sale_w)
            m_perc_arr[i].append(perc_sale_m)
            w_median_arr[i].append(tmp_w.filter(price_selection_metric=price_select_metrics['median'])[0].saleprice)
            m_median_arr[i].append(tmp_m.filter(price_selection_metric=price_select_metrics['median'])[0].saleprice)
            w_min_arr[i].append(tmp_w.filter(price_selection_metric=price_select_metrics['min'])[0].saleprice)
            m_min_arr[i].append(tmp_m.filter(price_selection_metric=price_select_metrics['min'])[0].saleprice)
            w_q75_arr[i].append(tmp_w.filter(price_selection_metric=price_select_metrics['q75'])[0].saleprice)
            m_q75_arr[i].append(tmp_m.filter(price_selection_metric=price_select_metrics['q75'])[0].saleprice)
            
    #print m_cnt_arr, w_cnt_arr, w_cnt_tarr, m_cnt_tarr
    json_str1 = get_barplot_jsonstrs(mcnt=m_perc_arr, fcnt=w_perc_arr)
    
    # Price and saleprice median
    json_str3 = get_barplot_ival_jsonstr(avg=w_median_arr, min=w_min_arr, max=w_q75_arr, gender='F')
    json_str4 = get_barplot_ival_jsonstr(avg=m_median_arr, min=m_min_arr, max=m_q75_arr, gender='M')
    
    #print json_str3, json_str4
    
    return render_to_response('gviz_stats.html', {'json1': json_str1['mcnt'], 
                                                  'json2': json_str1['fcnt'], 
                                                  'json3': json_str3,
                                                  'json4': json_str4,
                                                  'uid': userid}) 
    #return HttpResponse('OK')
