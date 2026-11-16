from django.db import models

# Create your models here.

from django.db import models

class Employee(models.Model):
    ename = models.CharField(max_length=100)  # Employee Name
    designation = models.CharField(max_length=100)  # Designation
    dob = models.DateField()  # Date of Birth
    email = models.EmailField()  # Email (which will also serve as the username)
    pno = models.IntegerField()  # Phone Number (which will also serve as password)
    address = models.TextField()  # Address
    username = models.CharField(max_length=50)  # Username (email field will be used)
    password = models.CharField(max_length=40)  # Password (phone number will be used)

    def __str__(self):
        return self.ename  # Return the name of the employee when the object is called
