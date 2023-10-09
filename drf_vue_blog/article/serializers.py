from rest_framework import serializers
from article.models import Article
# ### 原始寫法
# class ArticleListSerializer(serializers.Serializer):
    
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(allow_blank=True,max_length=100)
#     body = serializers.CharField(allow_blank=True)
#     created = serializers.DateTimeField()
#     updated = serializers.DateTimeField()

### 簡化器
from user_info.serializers import UserDescSerializer

class ArticleListSerializer(serializers.ModelSerializer):
    # read_only 參數設置為只讀
    # 序列化类我们已经比较熟悉了，这个序列化器专门用在文章列表中，展示用户的基本信息。
    # 最后修改文章列表的序列化器，把它们嵌套到一起：
    author = UserDescSerializer(read_only=True)

    class Meta:
        model = Article
        # fields = [
        #     "id",
        #     "title",
        #     "created",
        # ]
        fields = '__all__'

class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        # 此时在接收 POST 请求时，序列化器就不再理会请求中附带的 author 数据了：
        read_only_fields = ['author']




