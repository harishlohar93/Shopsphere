from django.contrib import admin
from .models import *



# Register your models here.


admin.site.register(Category)
admin.site.register(ProductImage)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price']
    inlines = [ProductImageAdmin]

admin.site.register(Product , ProductAdmin)

@admin.register(ColorVariant)
class ColorVarientAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']
    inlines = [ProductImageAdmin]
    
@admin.register(SizeVariant)    
class SizeVarientAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price']
    inlines = [ProductImageAdmin]    
