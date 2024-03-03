from rest_framework import (
    serializers,
)
from Account_Module.models import (
    User,
    Profile,
)
from django.contrib.auth.password_validation import (
    validate_password,
)
from django.contrib.auth import (
    authenticate,
)
from django.utils.translation import (
    gettext_lazy as _,
)
from django.core import (
    exceptions,
)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)


class CreateSuperUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        max_length=250,
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "phone",
            "email",
            "password",
            "re_password",
        ]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("re_password"):
            raise serializers.ValidationError(
                {"password": "password docent match"}
            )

        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop(
            "re_password",
            None,
        )

        return User.objects.create_superuser(**validated_data)


class RegistrationSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        max_length=250,
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "phone",
            "email",
            "password",
            "re_password",
        ]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("re_password"):
            raise serializers.ValidationError(
                {"password": "password docent match"}
            )

        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(
        self,
        validated_data,
    ):
        validated_data.pop(
            "re_password",
            None,
        )
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    phone = serializers.CharField(
        label=_("phone"),
        write_only=True,
    )
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True,
    )

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        if phone and password:
            user = authenticate(
                request=self.context.get("request"),
                phone=phone,
                password=password,
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(
                    msg,
                    code="authorization",
                )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(
                msg,
                code="authorization",
            )

        attrs["user"] = user
        return attrs


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validate_data = super().validate(attrs)
        validate_data["email"] = self.user.email
        validate_data["user_id"] = self.user.id
        return validate_data


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    re_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("re_new_password"):
            raise serializers.ValidationError(
                {"password": "password docent match"}
            )

        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )

        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        source="user.email",
        read_only=True,
    )

    class Meta:
        model = Profile
        fields = [
            "id",
            "email",
            "image",
            "first_name",
            "last_name",
            "description",
            "created_date",
        ]


class ActivationResendTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "User dose not exist "}
            )
        if user_obj.is_verified:
            raise serializers.ValidationError(
                {"detail": "User is already verified "}
            )
        print(user_obj)
        attrs["user"] = user_obj
        return super().validate(attrs)


class ResetPasswordSendTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "User dose not exist "}
            )
        attrs["user"] = user_obj
        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=250,
        write_only=True,
    )
    re_password = serializers.CharField(
        max_length=250,
        write_only=True,
    )

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("re_password"):
            raise serializers.ValidationError(
                {"password": "password does not match"}
            )

        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)
