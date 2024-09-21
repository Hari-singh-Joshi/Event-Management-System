from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


CATEGORY_CHOICES = [
    ('booked', 'Booked'),
    ('canceld', 'Canceled'),
    ('progress', 'Progress'),
    ('deleted', 'Deleted'),
    ('delivered', 'Delivered'),
]
class Vendor(models.Model):
    name = models.CharField(max_length=100)


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    
    Description = models.TextField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='activate')
    image = models.ImageField(upload_to='product_images/')
    vendor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name






class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity*self.product.Price


