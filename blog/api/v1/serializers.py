from rest_framework import serializers
from blog.models import Post, Category
from accounts.models import Profile


# class PostSer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=250)
class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet")  # show pease of content
    relative_url = serializers.ReadOnlyField(
        source="get_absolute_api_url"
    )  # show url of object
    absolute_url = serializers.SerializerMethodField()  # show url of object completely
    # category = serializers.SlugRelatedField(many=False, slug_field='name', queryset=Category.objects.all()) #show name of category instead off id
    # category = CategorySer() #another way to show category

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "status",
            "snippet",
            "category",
            "image",
            "relative_url",
            "absolute_url",
        ]
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):  # for change in show items
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request.parser_context.get("kwargs").get(
            "pk"
        ):  # check request for list or single item
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("content", None)
        rep["category"] = CategorySer(
            instance.category, context={"request": request}
        ).data  # another way to show category
        return rep

    def create(self, validated_data):  # call when create object
        """for choose user automatic"""

        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)
