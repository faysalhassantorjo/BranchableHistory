from django.contrib import admin

# Register your models here.
import nested_admin

from .models import Event, Actor

@admin.register(Event)
class EventAdmin(nested_admin.NestedModelAdmin):
    list_display = ["title", "branch", "time_label"]
    list_filter = ["branch", "time_label"]
    search_fields = ["title", "branch__name"]
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        (None, {
            "fields": ["title", "slug", "branch", "time_label", "date_label", "location", "content", "summary", "actors","writer", "prev_event"],
        }),
    )
    