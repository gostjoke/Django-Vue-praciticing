from rest_framework import serializers

from comment.models import Comment
from user_info.serializers import UserDescSerializer

class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    author = UserDescSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'created':{'read_only':True}}


# 跟之前一样， url 超链接字段让接口的跳转更方便，author 嵌套序列化器让显示的内容更丰富。
# 最后让评论通过文章接口显示出来：




