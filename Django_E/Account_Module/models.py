import datetime
import os
import random
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

import re


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    BASE_LIST = "0123456789abcdefghijklmnopqrstuvwxyz"
    new_name = "".join(random.choices(BASE_LIST, k=10))
    name, ext = get_filename_ext(filename)
    x = datetime.datetime.now()
    final_name = f"Profile/{x.year}/{x.month}/{x.day}/{new_name}{ext}"
    return f"Media/{final_name}"


def normalize_mobile(phone):
    regex = r"\w{2,4}\w{5}\w{1,2}"
    phone_number = str(phone)
    normal_phone = re.search(regex, phone_number)
    phone = normal_phone.group()
    return int(phone)


class UserManager(BaseUserManager):
    def create_user(self, phone, password, email, **extra_fields):
        if not phone:
            raise ValueError(_("the phone must be set"))
        phone = normalize_mobile(phone)
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, email, **extra_fields):
        user = self.create_user(
            phone, password=password, email=email, **extra_fields
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.IntegerField(unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to=upload_image_path, blank=True, null=True
    )
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name + " " + self.last_name} - {self.user.email}'
        return f"{self.user.phone} - {self.user.email}"


@receiver(post_save, sender=User)
def Save_Profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
