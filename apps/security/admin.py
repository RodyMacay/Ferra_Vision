from django.contrib import admin

from ..security.models import User,UserGroup, UserPermission
# Register your models here.

@admin.register(User)
class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'cedula', 'phone']
    search_fields = ['username', 'email', 'cedula', 'phone']
    list_filter = ['groups', 'user_permissions']

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['user', 'group']
    list_filter = ['user', 'group']
    search_fields = ['user__username', 'group__name']
    
@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'permission']
    list_filter = ['user', 'permission']
    search_fields = ['user__username', 'permission__name']



