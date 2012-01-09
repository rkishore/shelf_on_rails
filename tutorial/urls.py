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
    #(r'^wishlist/(\d{2,3})/$', 'polls.views.render_result_list'),
    (r'^wishlist/(\d{2,3})/$', 'polls.views.render_result_table'),
    (r'^wishlist/$', 'polls.views.wishlist'),
    #(r'^wishlist2/(\d+)/$', 'polls.views.wishlist2'),
    (r'^wishlist2/$', 'polls.views.wishlist2'),
    #(r'^item_list/', 'polls.views.render_result_list'),
    (r'^result/$', 'polls.views.result'),
    (r'^items/$', list_detail.object_list, items_info),
    (r'^admin/', include(admin.site.urls)),
    (r'^wishlist/(\d{2,3})/add_item_(\d+)_(\d{1,2})/$', 'polls.views.add_item_to_selected_items_list'),
    (r'^wishlist/(\d{2,3})/show_selected_items/$', 'polls.views.show_selected_items_new'),
    (r'^wishlist/(\d{2,3})/show_selected_items/apply_discount/$', 'polls.views.apply_discount'),
    (r'^graph/$', 'polls.views.testing_graphs'),
    (r'^wishlist2/(\d{2,3})/$', 'polls.views.render_result_table'),
    (r'^wishlist2/(\d{2,3})/add_item_(\d+)_(\d{1,2})/$', 'polls.views.add_item_to_selected_items_list'),
    (r'^wishlist2/(\d{2,3})/show_selected_items/$', 'polls.views.show_selected_items_new'),
    (r'^wishlist2/(\d{2,3})/show_selected_items/apply_discount/$', 'polls.views.apply_discount'),
    (r'^compare_promo/$', 'polls.views.compare_promo'),
    (r'^compare_pricerange/$', 'polls.views.compare_pricerange'),
    (r'^mock_wishlist/start/$', 'polls.view_mock_wishlist.start'),
)
