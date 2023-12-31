# Generated by Django 4.2.2 on 2023-09-19 09:52

import Blog_Module.models
from django.db import (
    migrations,
    models,
)
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        (
            "Account_Module",
            "0001_initial",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=250),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=Blog_Module.models.upload_image_path,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=Blog_Module.models.upload_image_path,
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=250),
                ),
                (
                    "content",
                    models.TextField(),
                ),
                (
                    "status",
                    models.BooleanField(),
                ),
                (
                    "created_date",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "updated_date",
                    models.DateTimeField(auto_now=True),
                ),
                (
                    "published_date",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Account_Module.profile",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="Category_Post",
                        to="Blog_Module.category",
                    ),
                ),
            ],
        ),
    ]
