from django.contrib import admin
from .models import Branch

# Register your models here.


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["name", "chronology", "is_main"]
    list_filter = ["chronology", "is_main"]
    search_fields = ["name", "chronology__title"]
    prepopulated_fields = {"slug": ("name",)}

    ordering = ["name"]
