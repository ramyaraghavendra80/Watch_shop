from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Watchlist,Wishlist, CustomUser, Profile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'phone_number', 'is_staff']
    search_fields = ['email', 'username']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('phone_number',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

admin.site.register(CustomUser, CustomUserAdmin)

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['brand', 'price', 'stock', 'discount']

admin.site.register(Watchlist, WatchlistAdmin)

