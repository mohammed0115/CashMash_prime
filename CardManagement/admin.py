from django.contrib import admin

# Register your models here.

from .models import Card


class PageAdmin(admin.ModelAdmin):


    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        self.search_fields  = [field.name for field in model._meta.fields if field.name != "id"]
        super(PageAdmin, self).__init__(model, admin_site)

# admin.site.register(Users,PageAdmin)
admin.site.register(Card,PageAdmin)