from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'birth_date', 'is_staff', 'is_active', 'is_verified', 'profile_image')
    list_filter = ('is_staff', 'is_active', 'is_verified')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'birth_date','password','profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'profile_image', 'birth_date','password1', 'password2', 'is_staff', 'is_active', 'is_superuser',' is_verified')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    # inlines = (BookInline,)

admin.site.register(CustomUser, CustomUserAdmin)