from django.db import models
from django.utils import timezone
import random
import string

from django.db import models
from django.db.models import Max
from django.utils import timezone

class Invoice(models.Model):
    
    invoice_id = models.CharField(max_length=20, primary_key=True, editable=False)
    date = models.DateField(default=timezone.now)
    customer_phone = models.CharField(max_length=15, null=True, blank=True)  
    created_at = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    
  
    
    
    
   
    
    def generate_invoice_id(self):
        """
        Generates a custom sequential invoice ID in the format of 'INV-00001', 'INV-00002', etc.
        """
        prefix = "INV-"
        padding_length = 5  # Number of digits for zero padding
        
        # Get the last invoice ID in the database
        last_invoice = Invoice.objects.aggregate(Max('invoice_id'))
        last_invoice_id = last_invoice.get('invoice_id__max', None)
        
        if last_invoice_id:
            # Extract the numeric part of the last invoice ID (e.g., from 'INV-00005' -> 5)
            last_number = int(last_invoice_id.split('-')[1])  # Assuming the format 'INV-00005'
            next_number = last_number + 1  # Increment the last number by 1
        else:
            # If there are no invoices yet, start with 1
            next_number = 1
        
        # Format the next invoice number with zero-padding
        next_invoice_id = f"{prefix}{next_number:0{padding_length}d}"
        return next_invoice_id

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically generate the invoice_id
        before saving the instance to the database.
        """
        if not self.invoice_id:
            self.invoice_id = self.generate_invoice_id()  # Assign a custom invoice ID before saving
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_id} - {self.customer_phone or 'No Phone'}"

from django.db import models

from django.db import models
from stockmanager.models import Product  # Assuming Product model is in stockmanager app

class InvoiceDetail(models.Model):
    # Foreign Key linking to the Invoice model
    invoice_id = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='products')
    
    # Product Name
    product_name = models.CharField(max_length=255)
    
    # Price of the product
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    # Quantity of the product
    quantity = models.DecimalField(max_digits=10, decimal_places=3,null=True)
    
    # Amount for the product (can be set manually)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    # Profit field
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,null=True)

    def __str__(self):
        return f"{self.product_name} (Invoice {self.invoice_id.invoice_id})"

    def save(self, *args, **kwargs):
        # Fetch the Product object based on the product name
        try:
            product = Product.objects.get(product_name=self.product_name)
            buying_price = product.buying_price  # Assuming the Product model has a 'buying_price' field
            
            # Calculate the profit based on the formula
            self.profit = self.amount - (self.quantity * buying_price)
        except Product.DoesNotExist:
            self.profit = 0.00  # If no product is found, default profit is 0.00
            
        # Call the original save method
        super().save(*args, **kwargs)

from datetime import datetime
class Returns(models.Model):
    invoice_id = models.CharField(max_length=20, primary_key=True, editable=False)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    date=models.DateField(default=datetime.now(),null=False,blank=False)

    
  
    
 

