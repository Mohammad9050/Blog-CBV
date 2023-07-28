from django.urls import path
from . import views

# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (  # jwt
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", views.RegisterApiView.as_view(), name="register"),
    # token login
    # path('token/login/', views.CustomAuthToken.as_view(), name='login-token'), # we overwrite this class in view . you can use just ObtainAuthToken in url
    # path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='logout-token'),
    # jwt
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "change_password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    # profile
    path("profile/", views.ProfileView.as_view(), name="profile"),
    # email
    path("test-email/", views.SendEmailTest.as_view(), name="send-email"),
    path(
        "activation-code/<str:token>",
        views.ActivationApiView.as_view(),
        name="active-code",
    ),
    path("resend-activation", views.ActivationResend.as_view(), name="resend"),
    path("reset-password/", views.ResetPassword.as_view(), name="reset_password"),
    path(
        "reset-password/<str:token>",
        views.ResetPassword2.as_view(),
        name="reset_password2",
    ),
]
