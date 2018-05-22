from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'state', 'member_id', 'sex', )
    readonly_fields = ('last_login', 'pw_changed_at', 'password', 'username', 'user_permissions', )

    def has_add_permission(self, request):
        return False
