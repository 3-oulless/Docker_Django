from django import (
    forms,
)
from .models import (
    User,
)


class LoginForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class CreateUserForm(forms.Form):
    phone = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    re_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data
        if self.cleaned_data["password"] != self.cleaned_data["re_password"]:
            raise forms.ValidationError("Passwords do not match")
        return data

    def clean_user(
        self,
    ):
        user_phone = self.cleaned_data.get("phone")
        user = User.objects.filter(phone=user_phone)
        if user.exists():
            raise forms.ValidationError("Phone Is Taken")
        return user_phone
