from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin
from .forms import UserCreationForm,UserChangeForm
from .models import User


class UserAdmin(UserBaseAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number','email','is_active','is_admin')
    list_filter = ('is_admin','is_active')

    fieldsets = (
        ('Specification',{'fields':('phone_number','email','full_name','password')}),
        ('Permissions',{'fields':('is_active','is_admin','last_login')})
    )

    add_fieldsets = (
        ('Specification',{'fields':('phone_number','email','full_name','password1','password2')}),
    )
    search_fields = ('email',)
    ordering = ('is_admin','is_active')
    filter_horizontal = []


admin.site.register(User,UserAdmin)
