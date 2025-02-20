from django.db import models
# Create your models here.

class doctor(models.Model):
    first_name=models.CharField(max_length=20)
    Last_name=models.CharField(max_length=20)
    profile_pic=models.ImageField(upload_to='doc_pics')
    username=models.CharField(max_length=20)
    email_id= models.EmailField(max_length = 254)
    password=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=15)
    state=models.CharField(max_length=15)
    pincode=models.IntegerField()

class patient(models.Model):
    first_name=models.CharField(max_length=20)
    Last_name=models.CharField(max_length=20)
    profile_pic=models.ImageField(upload_to='pat_pics')
    username=models.CharField(max_length=20)
    email_id= models.EmailField(max_length = 254)
    password=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=15)
    state=models.CharField(max_length=15)
    pincode=models.IntegerField()
