from django.conf.urls.defaults import patterns, include, url

from polls.models import Promoinfo, Items
from django.views.generic import list_detail


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

items_info = {
              "queryset" : Items.objects.all(),
              "template_name" : "items_list.html"
              #"template_object_name" : "something"
              }



urlpatterns = patterns('',
    # Example:
    # (r'^tutorial/', include('tutorial.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^date/', 'polls.views.current_datetime'),
    #(r'^wishlist/(?P<id_>\d{1,2,3})/', 'polls.views.render_result_list'),
    (r'^wishlist/(\d{2,3})/$', 'polls.views.render_result_list'),
    (r'^wishlist/$', 'polls.views.wishlist'),
    #(r'^item_list/', 'polls.views.render_result_list'),
    (r'^result/$', 'polls.views.result'),
    (r'^items/$', list_detail.object_list, items_info),
    (r'^admin/', include(admin.site.urls)),
)
