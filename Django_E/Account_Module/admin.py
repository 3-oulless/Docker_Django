from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import User, Profile


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [
        "phone",
        "email",
        "is_superuser",
        "is_active",
        "is_staff",
        "is_verified",
        "created_date",
    ]
    list_filter = ["is_active"]
    fieldsets = [
        ("Authentication", {"fields": ["phone", "email", "password"]}),
        (
            "Permissions",
            {
                "fields": [
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "is_verified",
                ]
            },
        ),
        ("Group_Permissions", {"fields": ["groups", "user_permissions"]}),
        ("Important Date", {"fields": ["last_login"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            "Authentication",
            {
                "classes": ["wide"],
                "fields": [
                    "phone",
                    "email",
                    "password1",
                    "password2",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "is_verified",
                ],
            },
        ),
    ]
    search_fields = ["phone"]
    ordering = ["phone"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)

admin.site.register(Profile)
