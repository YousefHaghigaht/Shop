from django.contrib import admin
from .models import Category,Product,Vote,Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','is_sub')
    prepopulated_fields = {'slug':['name']}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','is_available','views')
    raw_id_fields = ('category',)
    prepopulated_fields = {'slug':['name']}


admin.site.register(Vote)
