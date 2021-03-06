from django.contrib import admin

from plot.models import Plot

from ..admin_site import household_admin
from ..forms import HouseholdStructureForm
from ..models import HouseholdStructure
from .modeladmin_mixins import ModelAdminMixin


@admin.register(HouseholdStructure, site=household_admin)
class HouseholdStructureAdmin(ModelAdminMixin):

    form = HouseholdStructureForm
    date_hierarchy = 'modified'
    instructions = []
    list_display = (
        'household',
        'survey_schedule',
        # 'house',
        'enumerated',
        'enrolled',
        'refused_enumeration',
        # 'dashboard',
        'progress',
        'modified',
        'user_modified',
        'failed_enumeration_attempts')
    list_filter = (
        'survey_schedule',
        'progress',
        'enumerated',
        'enrolled',
        'refused_enumeration',
        'household__plot__map_area',
        'enrolled_datetime',
        'modified',
        'user_modified',
        'hostname_modified',
        'failed_enumeration_attempts',
    )
    search_fields = (
        'household__household_identifier',
        'household__id',
        'id',)
    readonly_fields = ('survey_schedule', )
    list_per_page = 15

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "plot":
            if request.GET.get('plot'):
                kwargs["queryset"] = Plot.objects.filter(
                    id__exact=request.GET.get('plot', 0))
        return super(HouseholdStructureAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
