from debra.models import Items, Brands, Categories
from debra.models import Promoinfo, ProductModel, CategoryModel, ColorSizeModel
from django.contrib import admin

admin.site.register(Promoinfo)
admin.site.register(Items)
admin.site.register(Brands)
admin.site.register(Categories)

admin.site.register(ProductModel)
admin.site.register(CategoryModel)
admin.site.register(ColorSizeModel)
