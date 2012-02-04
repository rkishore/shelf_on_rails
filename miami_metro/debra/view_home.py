# Create your views here.
import re
import os.path
from django.http import HttpResponse 
from django.shortcuts import render_to_response
from debra.models import UserIdMap

def get_js_shelfit_code(userid, server_name, server_port): 
    
    js_fname = os.path.join(os.path.dirname(__file__), '../jamie/shelfit.js').replace('\\','/')
    f = open(js_fname, 'r')
    js_str = f.read().replace("\n", " ").replace("\t", " ")
    js_str = re.sub(' +', ' ', js_str)
    js_str = re.sub('{{uid}}', str(userid), js_str)
    js_str = re.sub('servername', server_name, js_str)
    js_str = re.sub('serverport', server_port, js_str)
    return js_str

def home(request):
    
    try:
        ipaddr_csv = request.META['REMOTE_ADDR']    
    except KeyError:
        ipaddr = 'unknown'       
        return render_to_response('err_display.html', {'errmsg':6}) 
    else:
        print ipaddr_csv
        ipaddr = ipaddr_csv.split(',')[0]
        uid_obj = UserIdMap.objects.filter(ip_addr=ipaddr)
        if (uid_obj):
            userid = uid_obj[0].user_id
        else:
            uid_all = UserIdMap.objects.all()
            uid_new = UserIdMap()
            uid_new.ip_addr = ipaddr
            uid_new.user_id = len(uid_all) + 1 # this should be randomly generated integer for security but need to ensure uniqueness first
            uid_new.save()
            userid = uid_new.user_id
        
        server_name = request.META['SERVER_NAME']
        server_port = request.META['SERVER_PORT']
        js_str = get_js_shelfit_code(userid, server_name, server_port)
        print js_str
        
    return render_to_response('home.html', {'uid':userid, 'js_code': js_str, 'server_name': server_name, 'server_port': server_port})    

def reply_with_home(request, userid):
    try:
        server_name = request.META['SERVER_NAME']
        server_port = request.META['SERVER_PORT']
    except KeyError:
        return render_to_response('err_display.html', {'errmsg':6})
    
    js_str = get_js_shelfit_code(userid, server_name, server_port)
    print js_str
    return render_to_response('home.html', {'uid':userid, 'js_code': js_str, 'server_name': server_name, 'server_port': server_port})

def index(request):
    print 'In index'
    if 'member_id' in request.session:
        print request.session
        uid_obj = UserIdMap.objects.filter(user_id=request.session['member_id'])
        if (uid_obj):
            userid = uid_obj[0].user_id
            return reply_with_home(request, userid)
    else:
        if request.method == 'POST':
            uid_all = UserIdMap.objects.all()
            uid_new = UserIdMap()
            try:
                ipaddr_csv = request.META['REMOTE_ADDR']    
            except KeyError:
                ipaddr = 'unknown'       
                return render_to_response('err_display.html', {'errmsg':6}) 
            print ipaddr_csv
            ipaddr = ipaddr_csv.split(',')[0]
            uid_new.ip_addr = ipaddr
            uid_new.user_id = len(uid_all) + 1 # this should be randomly generated integer for security but need to ensure uniqueness first
            uid_new.save()
            userid = uid_new.user_id
            request.session['member_id'] = userid
            print 'Created new session ID: ', request.session['member_id']
            return reply_with_home(request, userid)
        else:
            print 'Init'
            try:
                server_name = request.META['SERVER_NAME']
                server_port = request.META['SERVER_PORT']
            except KeyError:
                return render_to_response('err_display.html', {'errmsg':6})
            return render_to_response('index.html', {'server_name':server_name, 'server_port':server_port})
    