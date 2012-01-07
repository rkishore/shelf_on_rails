from polls.models import Poll, Items, Brands, Categories
from polls.models import Promoinfo
from django.contrib import admin

admin.site.register(Poll)
admin.site.register(Promoinfo)
admin.site.register(Items)
admin.site.register(Brands)
admin.site.register(Categories)

'''
class PromotionAdmin(admin.ModelAdmin):
    fieldsets = [
                 ('Basic', {'fields': ['store', 'issued', 
                                       'code', 'validity', 
                                       'where_avail', 'shipping',
                                       'sex_category', 'item_category']}),
                 ('Deals', {'fields': ['promo_type', 'disc_perc', 'disc_aggr_amount',
                                            'disc_aggr_low_bound', 'disc_add_perc']})
                 ]

admin.site.register(Promotion, PromotionAdmin)
'''
