from polls.models import Poll
from polls.models import Promoinfo
from django.contrib import admin

admin.site.register(Poll)
admin.site.register(Promoinfo)

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