from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'contact_email', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'contact_email', 'user__username')
