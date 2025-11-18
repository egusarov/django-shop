# apps/cart/models.py
from django.db import models
from django.conf import settings
from apps.products.models import Product

class CartModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)  # the same structure as session cart
    updated_at = models.DateTimeField(auto_now=True)
