from django.contrib import admin
from django.contrib.auth import get_user_model

from .forms import RequiredHoursAdminForm, WorkitemAdminForm
from .models import RequiredHours, Workitem, WorkedHoursStats


@admin.register(RequiredHours)
class RequiredHoursAdmin(admin.ModelAdmin):
    list_display = ('year', 'hours', 'missingHoursPrice', 'fromYearOfBirth', 'toYearOfBirth')
    form = RequiredHoursAdminForm


@admin.register(Workitem)
class WorkitemAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'duration_expected', 'due_at', 'max_assignees')
    form = WorkitemAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'created_by':
            kwargs['queryset'] = get_user_model().objects.filter(pk=request.user.id)
        return super(WorkitemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data['created_by'] = request.user
        request.GET = data
        return super(WorkitemAdmin, self).add_view(request, form_url="", extra_context=extra_context)


@admin.register(WorkedHoursStats)
class WorkedHoursStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'year', 'hoursConfirmed', 'hoursNotConfirmed')
    readonly_fields = ('user', 'year', 'hoursConfirmed', 'hoursNotConfirmed')
    list_display_links = None
    actions = None

    def has_add_permission(self, request):
        return False
