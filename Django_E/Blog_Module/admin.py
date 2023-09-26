from django.contrib import (
    admin,
)
from .models import (
    Post,
    Category,
)


class PostAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "title",
        "content",
        "status",
        "category",
        "published_date",
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
