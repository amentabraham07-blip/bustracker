from django.db import models
from .models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver  # Import the receiver decorator
from datetime import datetime


# Create your models here.
class category(models.Model):
    category=models.CharField(max_length=60)

    def __str__(self):
        return self.category  # Return the name of the category when the object is called
    
    
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(category, on_delete=models.SET_NULL, null=True, blank=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    low_quantity = models.FloatField()
    date = models.DateField(null=True, blank=True)
    tax=models.IntegerField(default=0)
    Return=models.CharField(max_length=10,default='no')

    def __str__(self):
        return self.product_name

# Signal to update the 'date' field when quantity is updated from zero to a non-zero value
@receiver(pre_save, sender=Product)
def update_date_on_quantity_update(sender, instance, **kwargs):
    if instance.pk:
        # Check if this is an update (not a new object) and quantity is being changed from 0 to a positive value
        old_instance = Product.objects.get(pk=instance.pk)
        if old_instance.quantity == 0 and instance.quantity > 0:
            instance.date = datetime.now().date()
    else:
        # If it's a new object with quantity > 0 and the quantity is not zero initially
        if instance.quantity > 0:
            instance.date = datetime.now().date()



class Wastage(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=8, decimal_places=3)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    loss = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    date = models.DateField(default=datetime.now(),editable=False)
    reason=models.TextField(default='null')

    def save(self, *args, **kwargs):
        # Auto-calculate loss before saving
        self.loss = float(self.quantity) * float(self.price)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} (Loss: ₹{self.loss})"