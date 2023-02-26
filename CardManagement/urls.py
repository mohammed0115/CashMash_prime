"""SADAD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from CardManagement.views import CardList,getCard
from django.views.decorators.csrf import csrf_exempt
# router.register(r'top_up', views.TopUpTransactionViewSet, basename='cardholder_top_up_transaction')
urlpatterns = [

    path("Card/",csrf_exempt(CardList.as_view()),name="consumer_api_CardList"),
    path("Cards/<int:id>/",csrf_exempt(getCard.as_view()),name="consumer_api_CardList1"),
        

    
]
