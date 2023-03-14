from django.db import models

# Create your models here.
class ebs_consumer(models.Model):
    END_POINT =models.CharField(max_length=500,null=True,default='https://172.16.199.1:8877/QAConsumer')
    APPLICATION_ID =models.CharField(max_length=100,default='ITQAN')
    VERIFY_SSL =models.BooleanField(default=False)
    TIMEOUT =models.IntegerField(default=60)
    TIME_ZONE =models.CharField(max_length=100,default='Africa/Khartoum')
class ModelPublickey(models.Model):
    start_date = models.DateField( auto_now=True, auto_now_add=True)
    expired = models.DateField(auto_now=False, auto_now_add=False)
    pubKeyValue =models.TextField("")
    responseCode = models.IntegerField()
    responseMessage =models.CharField( max_length=50)
    responseStatus  =models.CharField(max_length=50)