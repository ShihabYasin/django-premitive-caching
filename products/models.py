from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet, Manager
from django_lifecycle import LifecycleModel, hook, AFTER_DELETE, AFTER_SAVE
from django.utils import timezone


class CustomQuerySet(QuerySet):
    def update(self, **kwargs):
        cache.delete('product_objects')
        super(CustomQuerySet, self).update(updated=timezone.now(), **kwargs)


class CustomManager(Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)


class Product(LifecycleModel):
    title = models.CharField(max_length=200, blank=False)
    price = models.CharField(max_length=20, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomManager()

    class Meta:
        ordering = ['-created']

    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    def invalidate_cache(self):
       cache.delete('product_objects')
