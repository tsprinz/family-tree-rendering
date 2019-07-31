from datetime import date
from django.contrib import admin

from .models import Person

class DecadeListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'decade born'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        qs = model_admin.get_queryset(request)
        for x in range(1000, 3000, 10):
            if qs.filter(birth_date__gte=date(x, 1, 1),
                    birth_date__lte=date(x+9, 12, 31)).exists():
                        yield (str(x), str(x)+'s')
    
    def queryset(self, request, queryset):
        if 'decade' in request.GET:    
            if request.GET['decade'] == '0':
                return queryset.filter(birth_date__lt=date(1900, 1, 1))
            else:
                return queryset.filter(birth_date__gte=date(int(request.GET['decade']), 1, 1),
                                        birth_date__lte=date(int(request.GET['decade'])+9, 12, 31))


class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Names',               {'fields': ['first_name', 'middle_names', 'last_name', 'birth_name', 'display_name']}),
        ('Birth & Death',   {'fields': ['birth_date', 'parent_a', 'parent_b', 'death_date']}),
        ('Photo', {'fields': ['image', ]}),
    ]
    
    def gen_name(self, obj):
        return obj.last_name.upper() + ', ' + obj.first_name
    gen_name.short_description = 'Name'

    list_display = ('gen_name', 'middle_names', 'birth_name', 'display_name', 'birth_date', 'death_date', 'parent_a', 'parent_b', 'gender')
    list_filter = ('last_name', DecadeListFilter)
    search_fields =  ['first_name', 'middle_names', 'last_name', 'birth_name', 'display_name', 'parent_a', 'parent_b']
    autocomplete_fields = ['parent_a', 'parent_b']

admin.site.register(Person, PersonAdmin)