from django.contrib import admin
from EBS_CONSUMER_API.models import ebs_consumer
# Register your models here.
class ebs_consumerAdmin(admin.ModelAdmin):
    list_display = ('id', 'END_POINT', 'APPLICATION_ID', 'VERIFY_SSL', 'TIMEOUT', 'TIME_ZONE')

admin.site.register(ebs_consumer, ebs_consumerAdmin)
