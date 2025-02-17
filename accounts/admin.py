from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin
from .forms  import UserCreationForm,UserChangeForm
from .models import User,OtpCode
from django.contrib.auth.models import Group

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

    filter_horizontal = []
    ordering = ('is_admin','is_active')
    search_fields = ('phone_number','email')


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number','code','created')


admin.site.unregister(Group)
admin.site.register(User,UserAdmin)




