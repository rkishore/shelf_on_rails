from django.conf.urls.defaults import patterns, include, url

from tutorial import settings
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
    (r'^wishlist/(\d+)/$', 'polls.views.render_result_table'),
    (r'^wishlist/$', 'polls.views.wishlist'),
    #(r'^wishlist2/(\d+)/$', 'polls.views.wishlist2'),
    (r'^wishlist2/$', 'polls.views.wishlist2'),
    #(r'^item_list/', 'polls.views.render_result_list'),
    (r'^result/$', 'polls.views.result'),
    (r'^items/$', list_detail.object_list, items_info),
    (r'^admin/', include(admin.site.urls)),
    (r'^wishlist/(\d+)/add_item_(\d+)_(\d{1,2})/$', 'polls.views.add_item_to_selected_items_list'),
    (r'^wishlist/(\d+)/show_selected_items/$', 'polls.views.show_selected_items_new'),
    (r'^wishlist/(\d+)/show_selected_items/apply_discount/$', 'polls.views.apply_discount'),
    (r'^graph/$', 'polls.views.testing_graphs'),
    (r'^wishlist2/(\d{2,3})/$', 'polls.views.render_result_table'),
    (r'^wishlist2/(\d{2,3})/add_item_(\d+)_(\d{1,2})/$', 'polls.views.add_item_to_selected_items_list'),
    (r'^wishlist2/(\d{2,3})/show_selected_items/$', 'polls.views.show_selected_items_new'),
    (r'^wishlist2/(\d{2,3})/show_selected_items/apply_discount/$', 'polls.views.apply_discount'),
    (r'^compare_promo/$', 'polls.views.compare_promo'),
    (r'^compare_pricerange/$', 'polls.views.compare_pricerange'),
    (r'^mock_wishlist/start/$', 'polls.view_mock_wishlist.start'),
    #(r'^statsup/$', 'polls.views.stats_update'),
    #(r'^statsplot/$', 'polls.views.stats_plot'),
    (r'^mock_wishlist/fill_db/$', 'polls.view_mock_wishlist.fill_db'),
    (r'^shelfit/apply_discount/(\Wu{1})?$', 'polls.views.apply_discount_new'),
    (r'^shelfit/(\Wu{1}\W(http){1})?$', 'polls.views.shelfit'),
    #(r'^viewyourshelf/(\Wu{1}\W(\d+))?$', 'polls.views.yourshelf_concise'),
    (r'^viewyourshelf/(\Wu{1}\W(\d+))?$', 'polls.view_shelf.yourshelf_store_based'),
    (r'^viewyourshelf_cat/(\Wu{1}\W(\d+))?$', 'polls.view_shelf.yourshelf_category_based'),        
    (r'^viewyourshelf/detail/(\Wu{1}\W(\d+)\Ws{1}\W)?$', 'polls.views.yourshelf_detail'),
    (r'^viewyourshelf/apply_discount/(\Wu{1})?$', 'polls.views.apply_discount_new'),
    (r'^home[\w\d.]*', 'polls.views.home'),
    (r'^create_wishlist/', 'polls.views.create_wishlist'),
    (r'^apply_promo/(\Wu{1}\W(\d+))?$', 'polls.view_shelf.apply_promo'),
    (r'^view_promo/', 'polls.views.view_promo'),
    (r'^add_bookmarklet/', 'polls.views.add_shelfit_bmarklet'),
    (r'^statsup/$', 'polls.views.stats_update_db'),
    (r'^statsplot/$', 'polls.views.stats_plot_from_db'),
    (r'^mymedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^display_meta/$', 'polls.views.display_meta'),
)
