from django.contrib import admin
from .models import Product, Variations, ReviewRating

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_stock' , 'category', 'id')
    prepopulated_fields = {'product_slug': ('product_name',)}
    list_filter = ('category',)
    

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variations, VariationAdmin)
admin.site.register(ReviewRating)



