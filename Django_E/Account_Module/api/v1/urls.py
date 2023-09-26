from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


app_name = "api_v1"


urlpatterns = [
    # create user
    path("register/", views.RegistrationApiView.as_view(), name="register"),
    # login Token
    path(
        "token/login/",
        views.CustomObtainAuthToken.as_view(),
        name="resend_token",
    ),
    path(
        "token/logout/",
        views.CustomDiscardAuthToken.as_view(),
        name="token_logout",
    ),
    # email send
    path(
        "resend_token/",
        views.ActivationResendTokenView.as_view(),
        name="verify_email",
    ),
    path(
        "email_activation/<str:token>",
        views.ActivationEmailView.as_view(),
        name="activation_email",
    ),
    # login JWT
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt_create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    # change password
    path(
        "change_password/",
        views.ChangePasswordView.as_view(),
        name="change_password",
    ),
    # reset password
    path(
        "reset_password_send_token/",
        views.ResetPasswordSendTokenView.as_view(),
        name="reset_password_send_token",
    ),
    path(
        "reset_password_check_token/<str:token>",
        views.ResetPasswordTokenCheckView.as_view(),
        name="reset_password_check_token",
    ),
    path(
        "reset_password/<int:pk>/",
        views.ResetPasswordView.as_view(),
        name="reset_password",
    ),
    # profile
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
