from rest_framework import (
    generics,
)

from Account_Module.models import (
    Profile,
    User,
)
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ActivationResendTokenSerializer,
    ResetPasswordSendTokenSerializer,
    ResetPasswordSerializer,
)

from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from rest_framework.authtoken.views import (
    ObtainAuthToken,
)
from rest_framework.authtoken.models import (
    Token,
)
from rest_framework.response import (
    Response,
)
from rest_framework import (
    status,
)
from rest_framework.views import (
    APIView,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from mail_templated import (
    EmailMessage,
)
from ..utils import (
    EmailSendThreading,
)
from rest_framework_simplejwt.tokens import (
    RefreshToken,
)
import jwt
from Django_E.settings import (
    SECRET_KEY,
)


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        srz = self.serializer_class(data=request.data)

        if srz.is_valid():
            srz.save()
            email = srz.validated_data.get("email")
            data = {"email": email}

            user_obj = get_object_or_404(
                User,
                email=email,
            )
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "Email/activation_email.tpl",
                {
                    "phone": user_obj.phone,
                    "token": token,
                },
                "admin@admi.com",
                to=[email],
            )
            EmailSendThreading(email_obj).start()

            return Response(
                data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            srz.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_tokens_for_user(self, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        srz = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        srz.is_valid(raise_exception=True)
        user = srz.validated_data.get("user")
        (
            token,
            created,
        ) = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "phone": user.phone,
                "email": user.email,
            }
        )


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(
        self,
        request,
    ):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        srz = self.serializer_class(data=request.data)

        srz.is_valid(raise_exception=True)

        if not user.check_password(srz.validated_data.get("password")):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(srz.validated_data.get("new_password"))
        user.save()
        return Response(
            {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(
        self,
    ):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            user=self.request.user,
        )
        return obj


class ActivationEmailView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token_decode = jwt.decode(
                jwt=token,
                key=SECRET_KEY,
                algorithms=["HS256"],
            )
            user_id = token_decode.get("user_id")
        except jwt.exceptions.ExpiredSignatureError:
            return Response(
                {"detail": "Token has ben expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.InvalidSignatureError:
            return Response(
                {"detail": "Token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"detail": "Token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = get_object_or_404(
            User,
            pk=user_id,
        )
        if user_obj.is_verified:
            return Response(
                {"detail": "Your Account has already been activated"},
                status=status.HTTP_202_ACCEPTED,
            )
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"detail": "Your Account activated"},
            status=status.HTTP_202_ACCEPTED,
        )


class ActivationResendTokenView(generics.GenericAPIView):
    serializer_class = ActivationResendTokenSerializer

    def post(self, request, *args, **kwargs):
        srz = ActivationResendTokenSerializer(data=request.data)
        srz.is_valid(raise_exception=True)
        user_obj = srz.validated_data.get("user")
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "Email/activation_email.tpl",
            {
                "phone": user_obj.phone,
                "token": token,
            },
            "admin@admi.com",
            to=[user_obj.email],
        )
        EmailSendThreading(email_obj).start()
        return Response(
            {"detail": "user activation resend successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)


class ResetPasswordSendTokenView(generics.GenericAPIView):
    serializer_class = ResetPasswordSendTokenSerializer

    def post(self, request, *args, **kwargs):
        srz = ResetPasswordSendTokenSerializer(data=request.data)
        srz.is_valid(raise_exception=True)
        user_obj = srz.validated_data.get("user")
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "ResetPassword/ResetPassword.tpl",
            {
                "phone": user_obj.phone,
                "token": token,
            },
            "admin@admi.com",
            to=[user_obj.email],
        )
        EmailSendThreading(email_obj).start()
        return Response(
            {"detail": "send email for reset password"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)


class ResetPasswordTokenCheckView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def get(self, request, token, *args, **kwargs):
        try:
            token_decode = jwt.decode(
                jwt=token,
                key=SECRET_KEY,
                algorithms=["HS256"],
            )
            user_id = token_decode.get("user_id")
        except jwt.exceptions.ExpiredSignatureError:
            return Response(
                {"detail": "Token has ben expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.InvalidSignatureError:
            return Response(
                {"detail": "Token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"detail": "Token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return redirect(
            "account:api_v1:reset_password",
            pk=int(user_id),
        )


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, pk, *args, **kwargs):
        srz = ResetPasswordSerializer(data=request.data)
        srz.is_valid(raise_exception=True)
        password = srz.validated_data.get("password")

        user_obj = get_object_or_404(
            User,
            pk=pk,
        )
        user_obj.set_password(password)
        user_obj.save()

        return Response(
            {"detail": "Your password has been successfully changed"},
            status=status.HTTP_200_OK,
        )
