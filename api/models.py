from django.db import models

# Create your models here.
class User(models.Model):
	token   = models.CharField(max_length=250)
	phone_number = models.CharField(max_length=15)
	totp         = models.CharField(max_length=5)
