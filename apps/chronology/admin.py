from django.contrib import admin
from .models import Chronology

# Register your models here.


@admin.register(Chronology)
class ChronologyAdmin(admin.ModelAdmin):
    list_display = ["title", "period", "created_by"]
    list_filter = ["created_by"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]
    prepopulated_fields = {"slug": ("title",)}
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'start_date', 'end_date', 'created_by')
        }),
    )
