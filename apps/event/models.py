from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from config.abstract_models import BaseModel
from django.utils.text import slugify
from apps.chronology.models import Chronology
from apps.branch.models import Branch


class Actor(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        unique_together = ["name"]
        indexes = [
            models.Index(fields=["name"]),
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


class Event(BaseModel):


    # Event details
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=255)
    date_label = models.DateTimeField() #exact date like Dec 17 2022
    time_label = models.CharField(max_length=255) #  "2010" year group label

    # Narrative
    content = models.TextField()
    summary = models.TextField()

    # Event relationships
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="events"
    )

    prev_event = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_event"
    )

    actors = models.ManyToManyField(
        Actor,
        related_name="events",
        blank=True
    )

    writer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events"
    )

    class Meta:
        unique_together = ["title",  "branch"]
        indexes = [
            models.Index(fields=["title", "branch"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().update(*args, **kwargs)
