from django.contrib import admin

from test_product.models import Attr, Product, ProductAttr, UniqueProduct


@admin.register(Attr)
class AttrAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProductAttr)
class ProductAttrAdmin(admin.ModelAdmin):
    list_display = ('attr', 'product', 'value',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(UniqueProduct)
class UniqueProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'attr', 'objects',)
