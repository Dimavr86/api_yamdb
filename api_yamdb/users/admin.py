
from django.contrib import admin
from .models import User


@admin.register(User)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'bio', 'role')
    list_filter = ('role', )
    list_display_links = list_display
    search_fields = ('user__username', 'user__first_name',
                     'user__last_name', 'user__email', 'role')
    
