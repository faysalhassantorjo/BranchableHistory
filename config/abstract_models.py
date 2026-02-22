from django.db import models
from django.utils import timezone
import uuid

class SoftDeleteQuerySet(models.QuerySet):
    def delete(self, deleted_by=None):
        return super().update(
            deleted_at=timezone.now(),
            deleted_by=deleted_by
        )

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)

    def restore(self):
        return self.update(deleted_at=None, deleted_by=None)

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def dead(self):
        return SoftDeleteQuerySet(self.model, using=self._db).dead()

    def all_with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        "auth.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="deleted_%(class)s_set"
    )

    objects = SoftDeleteManager()
    all_objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["deleted_at"]),
        ]

    # Soft delete (single object)
    def delete(self, using=None, keep_parents=False, deleted_by=None):
        self.deleted_at = timezone.now()
        self.deleted_by = deleted_by
        self.save(update_fields=["deleted_at", "deleted_by"])

    # Real delete
    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    # Restore
    def restore(self):
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=["deleted_at", "deleted_by"])

