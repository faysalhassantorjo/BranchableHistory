from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from config.abstract_models import BaseModel
from django.utils.text import slugify
from apps.chronology.models import Chronology



class Branch(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    chronology = models.ForeignKey(Chronology, on_delete=models.CASCADE, related_name="branches")
    is_main = models.BooleanField(default=False)


    initial_event = models.ForeignKey("event.Event", on_delete=models.SET_NULL, null=True, blank=True, related_name="branches")


    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_branches"
    )

    class Meta:
        unique_together = ["name", "chronology"]
        indexes = [
            models.Index(fields=["name", "chronology"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().update(*args, **kwargs)

