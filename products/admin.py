from django.contrib import admin
from .models import Category,Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','is_sub','sub_category')
    prepopulated_fields = {'slug':['name']}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','is_available','updated')
    list_filter = ('is_available','updated')
    prepopulated_fields = {'slug':['name']}
    raw_id_fields = ('category',)
