from rest_framework import serializers

from comment.models import Comment
from user_info.serializers import UserDescSerializer

class CommentChildrenSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    author = UserDescSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = [
            'parent',
            'article'
        ]

class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    author = UserDescSerializer(read_only=True)

    # new part of parent
    article = serializers.HyperlinkedRelatedField(view_name='article-detail', read_only=True)
    article_id = serializers.IntegerField(write_only=True, allow_null=False, required=True)

    # parent parts
    parent = CommentChildrenSerializer(read_only=True)
    parent_id = serializers.IntegerField(write_only = True, allow_null=True, required=False)

    def update(self, instance, validated_data):
        validated_data.pop('parent_id', None)
        return super().update(instance, validated_data)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'created':{'read_only':True}}


# 跟之前一样， url 超链接字段让接口的跳转更方便，author 嵌套序列化器让显示的内容更丰富。
# 最后让评论通过文章接口显示出来：




