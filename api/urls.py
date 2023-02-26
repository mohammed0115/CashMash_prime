from django.urls import path
from api.views import index,telecom,getbill,electricty,transfer,error,success,NotFound
urlpatterns = [
    path('index/', index,name='index'),
    path('telecom/', telecom,name='telecom'),
    path('getbill/', getbill,name='bill'),
    path('electricty/', electricty,name='electricty'),
    path('transfer/', transfer,name='transfer'),
    
    path('error/', error,name='error'),
    
    
    path('success/', success,name='success'),
    path('NotFound/', NotFound,name='NotFound'),
]