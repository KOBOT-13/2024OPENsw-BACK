from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class BookInline(admin.TabularInline):
    model = CustomUser.mybook_list.through
    extra = 1
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active', 'is_verified')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    inlines = (BookInline,)

admin.site.register(CustomUser, CustomUserAdmin)
