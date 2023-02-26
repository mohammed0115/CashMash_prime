from django.db import models

# Create your models here.
class ebs_consumer(models.Model):
    END_POINT =models.CharField(max_length=500,null=True,default='https://172.16.199.1:8877/QAConsumer')
    APPLICATION_ID =models.CharField(max_length=100,default='CashMash')
    VERIFY_SSL =models.BooleanField(default=False)
    TIMEOUT =models.IntegerField(default=60)
    TIME_ZONE =models.CharField(max_length=100,default='Africa/Khartoum')
