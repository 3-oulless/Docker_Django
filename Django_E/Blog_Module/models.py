import datetime
import os
import random
from django.db import (
    models,
)
from Account_Module.models import (
    Profile,
)
from django.urls import (
    reverse,
)


def get_filename_ext(
    filepath,
):
    base_name = os.path.basename(filepath)
    (
        name,
        ext,
    ) = os.path.splitext(base_name)
    return name, ext


def upload_image_path(
    instance,
    filename,
):
    BASE_LIST = "0123456789abcdefghijklmnopqrstuvwxyz"
    new_name = "".join(
        random.choices(
            BASE_LIST,
            k=10,
        )
    )
    (
        name,
        ext,
    ) = get_filename_ext(filename)
    x = datetime.datetime.now()
    final_name = (
        f"{instance.id}/{x.year}/{x.month}/{x.day}/{new_name}{ext}"
    )
    return f"Media/{final_name}"


class Post(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to=upload_image_path,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="Category_Post",
    )

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(
        self,
    ):
        return self.title

    def grt_snippet(
        self,
    ):
        return self.content[:6]

    def get_absolute_api_url(
        self,
    ):
        return reverse(
            "post:api_v1:post-detail",
            kwargs={"pk": self.id},
        )


class Category(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(
        upload_to=upload_image_path,
        null=True,
        blank=True,
    )

    def __str__(
        self,
    ):
        return self.name
