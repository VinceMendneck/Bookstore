from django.db import models

from .category import Category

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.PositiveIntegerField(null=True)
    active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, blank=True)