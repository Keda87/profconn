from django.contrib import admin

from .models import Person, Experience


class ExperienceTab(admin.TabularInline):
    model = Experience
    fields = ['company', 'role', 'start_date', 'end_date', 'description']
    extra = 0


class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = list_display
    fieldsets = [
        (None,          {'fields': ['name', 'email', 'birth', 'profile_picture']}),
        ('Information', {'fields': ['headline', 'bio'], 'classes': ['collapse']}),
    ]
    inlines = [ExperienceTab]

admin.site.register(Person, PersonAdmin)
