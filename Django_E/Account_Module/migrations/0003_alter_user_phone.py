# Generated by Django 3.2.24 on 2024-03-03 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Account_Module", "0002_alter_user_is_verified"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.BigIntegerField(unique=True),
        ),
    ]