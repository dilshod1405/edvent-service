from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Display in list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_verified','id',)
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    

    # Add 'photo' and 'role' to the form fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'photo')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'photo')}),
    )

    search_fields = ('username', 'email', 'role')
    ordering = ['id']
    list_editable = ('is_active', 'role',  'is_verified')