from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from config.abstract_models import BaseModel
from django.utils.text import slugify


class Chronology(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    prepopulated_fields = {"slug": ("title",)}

    start_date = models.CharField(max_length=255, null=True, blank=True)
    end_date = models.CharField(max_length=255, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["start_date", "end_date"]),
        ]

    @property
    def period(self):
        return f"{self.start_date} - {self.end_date}"
    


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().update(*args, **kwargs)
