from django.views.decorators.csrf import csrf_exempt
#from django.conf.urls import url,include
from django.urls import path,include
from accounts.views import (
    LoginUserView,
    LogoutUserView,
    RefreshUserTokenView,
    RegisterUserView,
    
)
from otp.views import GenerateOTPView, ResetPassword,VerifyOtpViews,RegisterOTpView,ChangePassword
urlpatterns = [
    path(
        "login/",
        csrf_exempt(LoginUserView.as_view()),
        name="consumer_api_user_login",
    ),
    path(
        "logout/",
        csrf_exempt(LogoutUserView.as_view()),
        name="consumer_api_user_logout",
    ),
    path(
        "register/",
        csrf_exempt(RegisterUserView.as_view()),
        name="consumer_api_user_register",
    ),
    path(
        "refresh_token/",
        csrf_exempt(RefreshUserTokenView.as_view()),
        name="consumer_api_refresh_token",
    ),
    path(
        "generate_otp/",
        csrf_exempt(GenerateOTPView.as_view()),
        name="consumer_api_generate_otp",
    ),
    path(
        "ResetPassword/",
        csrf_exempt(ResetPassword.as_view()),
        name="consumer_api_verify_otp",
    ),
    path(
        "VerifyOtp/",
        csrf_exempt(VerifyOtpViews.as_view()),
        name="consumer_api_ResetPassword",
    ),
    path(
        "RegisterOTp/",
        csrf_exempt(RegisterOTpView.as_view()),
        name="consumer_api_RegisterOTp",
    ),
    path(
        "ChangePassword/",
        csrf_exempt(ChangePassword.as_view()),
        name="consumer_api_ChangePassword",
    ),
    path('',include('CardManagement.urls')),
    # path(
    #     "Card/",csrf_exempt(CardList.as_view()),name="consumer_api_CardList",
    # ),
    # path(
    #     "Cards/<int:id>/",
    #     csrf_exempt(getCard.as_view()),
    #     name="consumer_api_CardList",
    # ),
    
    #getCard
]
