from rest_framework import (
    serializers,
)
from Blog_Module.models import (
    Post,
    Category,
)
from Account_Module.models import (
    Profile,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "image",
        ]


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="grt_snippet")
    relative_url = serializers.URLField(
        source="get_absolute_api_url",
        read_only=True,
    )
    absolute_url = serializers.SerializerMethodField(
        method_name="get_abs_url"
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "image",
            "snippet",
            "content",
            "category",
            "status",
            "absolute_url",
            "relative_url",
            "created_date",
            "published_date",
        ]
        read_only_fields = ["author"]

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(
        self,
        instance,
    ):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop(
                "absolute_url",
                None,
            )
            rep.pop(
                "relative_url",
                None,
            )
            rep.pop(
                "snippet",
                None,
            )
        else:
            rep.pop(
                "content",
                None,
            )

        rep["category"] = CategorySerializer(
            instance.category,
            context={"request": request},
        ).data
        return rep

    def create(
        self,
        validated_data,
    ):
        if self.context.get("request").user.id is not None:
            validated_data["author"] = Profile.objects.get(
                user_id=self.context.get("request").user.id
            )
        else:
            raise serializers.ValidationError(
                {"detail": "User is not authenticated"}
            )
        return super().create(validated_data)
