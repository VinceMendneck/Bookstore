from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from product.models import Product

class Order(models.Model):
    product = models.ManyToManyField(Product, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    
    def clean(self):
        if not self.product.exists():
            raise ValidationError("At least one product is required.")
    
    def __str__(self):
        return f"Order for {self.user.username}"