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
from Consumer import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'CashMash Prime'
admin.site.index_title = 'CashMash Prime'                 # default: "Site administration"
admin.site.site_title = 'CashMash Prime' 
admin.autodiscover()
router = DefaultRouter()
# router.register(r'top_up', views.TopUpTransactionViewSet, basename='cardholder_top_up_transaction')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('PayeeList/', views.PayeeListView.as_view()),
    path('CardTransfer/', views.CardTransferView.as_view()),
    path('Balance/',csrf_exempt(views.balance_inquiry_for_PAN)),
    path('isAlive/', csrf_exempt(views.echoTest)),
    path('phone/Balance/', csrf_exempt(views.balance_inquiry_for_phone)),
    path('GetPublicKey/',csrf_exempt(views.get_public_key)),
    path('TransactionStatus/', views.TransactionStatusView.as_view()),
    path('Payment/',views.PaymentView.as_view()),
    path('ServicePayment/', views.ServicePaymentView.as_view()),
    path('GetBill/', views.GetBill.as_view()),
    path('GenerateVoucher/', views.GenerateVoucherView.as_view()),
    path('', include('api.urls')),
    #balance_inquiry_for_PAN
    path('EchoTest/', views.EchoTestView.as_view()),
    path('RequestPinChange/', views.RequestPinChangeView.as_view()),
    path('Regsiter/', csrf_exempt(views.Regsiter)),
    path('completeCardRegistration/', views.completeCardRegistration.as_view()),
    path('forgetPassword/', views.forgetPassword.as_view()),
    path('changePassword/', views.changePassword.as_view()),
    path('doQRPurchase/', views.doQRPurchase.as_view()),
    path('doQRRefund/', views.doQRRefund.as_view()),
    path('accounts/', include('accounts.urls')),
    # path('/', include('accounts.urls')),



    path('Card/', include('registerCard.urls')),
        

    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
