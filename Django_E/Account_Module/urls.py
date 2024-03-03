from django.urls import (
    path,
    include,
)
from .views import login_user, CreateUser, send_email

app_name = "account"

urlpatterns = [
    path(
        "login/",
        login_user,
        name="login",
    ),
    path("send-email/", send_email, name="send_email"),
    path(
        "create/",
        CreateUser.as_view(),
        name="create",
    ),
    # serializer
    path(
        "api/v1/",
        include(
            "Account_Module.api.v1.urls",
            namespace="api_v1",
        ),
    ),
]
