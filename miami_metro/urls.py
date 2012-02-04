from django.conf.urls.defaults import patterns, include, url
from miami_metro import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'miami_metro.views.home', name='home'),
    # url(r'^miami_metro/', include('miami_metro.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Media-related routing
    (r'^mymedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    # Home-related routing
    ('^$', 'debra.view_home.index'),
    (r'^home/$', 'debra.view_home.home'),
    
    # Stats-related routing 
    (r'^statsup/$', 'debra.view_stats.update_db'),
    (r'^statsplot/$', 'debra.view_stats.plot_from_db'),
    
    # Shelf-related routing
    (r'^shelfit/(\Wu{1}\W(http){1})?$', 'debra.view_shelf.shelfit'),
    (r'^viewyourshelf/(\Wu{1}\W(\d+))?$', 'debra.view_shelf.yourshelf_store_based'),
    (r'^viewyourshelf_cat/(\Wu{1}\W(\d+))?$', 'debra.view_shelf.yourshelf_category_based'),        
    
    # Promo-related routing
    (r'^apply_promo/(\Wu{1}\W(\d+))?$', 'debra.view_shelf.apply_promo'),
    
    # Remove-item-related routing
    (r'^delitem/(\Wu{1}\W(\d+))?$', 'debra.view_shelf.remove_item'),
)
