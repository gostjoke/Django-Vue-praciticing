from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import Http404

# from django.shortcuts import render
from django.http import JsonResponse
from article.models import Article
# Create your views here.
from article.serializers import ArticleListSerializer

# 权限控制
# DRF 内置了如 IsAuthenticated、IsAdminUser、AllowAny 等权限控制类。

# 由于是个人博客，因此只准许管理员发布文章。修改文章列表视图如下：

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions

### traditional
# def a_list(request):
#     articles = Article.objects.all()
#     return render(..., context={'articles': articles})

### 進階寫法
# def article_list(request):
#     articles = Article.objects.all()

#     serializer = ArticleListSerializer(articles, many=True)
#     return JsonResponse(serializer.data, safe=False)
########################################################################
### 運用api_view 寫法
# @api_view(['GET', 'POST'])
# def article_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all() 
#         serializer = ArticleListSerializer(articles, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = ArticleListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
### 進階封裝寫法
from rest_framework import mixins
from rest_framework import generics

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """ 
    only管理員用戶可以修改 
    or 員工
    the ther user can see
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_superuser or request.user.is_staff



class article_list(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer

    # 新增 權限
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

########################################################################
## base on httpie    
## http POST http://127.0.0.1:8000/api/article/ title=PostByJson body=HelloWorld!

from rest_framework.views import APIView
from article.serializers import ArticleDetailSerializer

### 原始寫法
# class ArticleDetail(APIView):
#     """ 文章詳情視圖"""
    
#     def get_object(self, pk):
#         try:
#             # pk 即主键，默认状态下就是 id
#             return Article.objects.get(pk=pk)
#         except:
#             raise Http404

#     def get(self, request, pk):
#         article = self.get_object(pk)

#         serializer = ArticleDetailSerializer(article)
#         # 返回 Json 数据
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleDetailSerializer(article, data=request.data)
#         # 驗證提交數據合法
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
#     def delete(self, request, pk):
#         article = self.get_object(pk)
#         article.delete()
#         # if delete success return 204
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

## 对数据的增删改查是几乎每个项目的通用操作，因此可以通过 DRF 提供的 Mixin 类直接集成对应的功能。



# class ArticleDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleDetailSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

### 更簡化的寫法

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUserOrReadOnly]
########################################################################

### 视图集类把前面章节写的列表、详情等逻辑都集成到一起，并且提供了默认的增删改查的实现。
from rest_framework import viewsets
from article.serializers import ArticleSerializer
from rest_framework import filters

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    # 如果要实现更常用的模糊匹配，就可以使用 SearchFilter 做搜索后端：
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_serializer_class(self):
    ### 對應到不同的權限
    #     if self.action == 'list':
    #         return SomeSerializer
    #     else:
    #         return AnotherSerializer

    # 我们可以覆写 get_queryset() 方法来实现过滤：
    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get('username', None)
        
        if username is not None:
            queryset = queryset.filter(author__username = username)

        return queryset

# 视图集
from article.models import Category
from article.serializers import CategorySerializer, CategoryDetailSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """ 分類視圖集 """
    queryset = Category.objects.all()
    serializer_class =CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer