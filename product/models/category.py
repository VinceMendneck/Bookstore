from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField( unique=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    