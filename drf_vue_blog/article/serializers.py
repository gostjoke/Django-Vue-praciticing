from rest_framework import serializers
from article.models import Article, Category




# ### 原始寫法
# class ArticleListSerializer(serializers.Serializer):
    
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(allow_blank=True,max_length=100)
#     body = serializers.CharField(allow_blank=True)
#     created = serializers.DateTimeField()
#     updated = serializers.DateTimeField()

### 簡化器
from user_info.serializers import UserDescSerializer

# class ArticleListSerializer(serializers.ModelSerializer):
#     # read_only 參數設置為只讀
#     # 序列化类我们已经比较熟悉了，这个序列化器专门用在文章列表中，展示用户的基本信息。
#     # 最后修改文章列表的序列化器，把它们嵌套到一起：
#     author = UserDescSerializer(read_only=True)

#     class Meta:
#         model = Article
#         # fields = [
#         #     "id",
#         #     "title",
#         #     "created",
#         # ]
#         fields = '__all__'

class ArticleListSerializer(serializers.ModelSerializer):
    # 新增字段，添加超链接
    url = serializers.HyperlinkedIdentityField(view_name="article:detail")

    class Meta:
        model = Article
        fields = [
            # 有了 url 之后，id 就不需要了
            'url',
            # 'id',
            # "title",
            # "created",
        ]
from comment.serializers import CommentSerializer


# class ArticleDetailSerializer(serializers.ModelSerializer):

#     id = serializers.IntegerField(read_only=True)
#     comments = CommentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Article
#         fields = '__all__'
#         # 此时在接收 POST 请求时，序列化器就不再理会请求中附带的 author 数据了：
#         read_only_fields = ['author']

### 新增Category
class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name ='category-detail')

    class Meta:
        model = Category
        fields = '__all__'

### 新增tag
from article.models import Tag
class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = UserDescSerializer(read_only=True)
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    # tag 字段
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )

    # 覆写方法，如果输入的标签不存在则创建它
    """
    to_internal_value() 方法原本作用是将请求中的原始 Json 数据转化为 Python 表示形式（期间还会对字段有效性做初步检查）。
    它的执行时间比默认验证器的字段检查更早, 因此有机会在此方法中将需要的数据创建好, mkkm然后等待检查的降临。isinstance() 确定标签数据是列表
    ，才会循环并创建新数据。
    """
    def to_internal_value(self, data):
        tags_data = data.get('tags')

        if isinstance(tags_data):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)
            
        return super().to_internal_value(data)

    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists() and value is not None:
            raise serializers.ValidationError("Category with id {} not exists.".format(value))
        return value            

    class Meta:
        model = Article
        fields = '__all__'

class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """给分类详情的嵌套序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = [
            'url',
            'title',
        ]

class CategoryDetailSerializer(serializers.ModelSerializer):
    """分类详情"""
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'created',
            'articles',
        ]


from article.models import Avatar

class AvatarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'


# 将已有的 ArticleSerializer 里的东西全部挪到这个 ArticleBaseSerializer 里来
# 除了 Meta 类保留
class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = UserDescSerializer(read_only=True)
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    # tag 字段
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )

    def to_internal_value(self, data):
        tags_data = data.get('tags')

        if isinstance(tags_data):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)
            
        return super().to_internal_value(data)

    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists() and value is not None:
            raise serializers.ValidationError("Category with id {} not exists.".format(value))
        return value            


# 保留 Meta 类
# 将父类改为 ArticleBaseSerializer
class ArticleSerializer2(ArticleBaseSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'body': {'write_only': True}}

class ArticleDetailSerializer(ArticleBaseSerializer):
    # 渲染后的正文
    id = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    body_html = serializers.SerializerMethodField()
    # 渲染后的目录
    toc_html = serializers.SerializerMethodField()

    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'