from django.contrib import admin

from .models import Company

class CompanyAdmin(admin.ModelAdmin):
    exclude = ['created', 'modified', 'is_deleted', 'uuid']
    search_fields = ['name']

admin.site.register(Company, CompanyAdmin)
