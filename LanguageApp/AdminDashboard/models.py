from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField(unique=True)
    roll = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    dob = models.DateField()
    phone = models.CharField(max_length=15)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    

    def __str__(self):
        return self.username
    
class Language(models.Model):
    language=models.CharField(max_length=100)
    def __str__(self):
        return self.language
