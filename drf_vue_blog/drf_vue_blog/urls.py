"""drf_vue_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api-auth/', include('rest_framework.urls')),
#     path('api/article/', include('article.urls', namespace='article')),
    
# ]

from rest_framework.routers import DefaultRouter
from article import views
from django.conf import settings
from django.conf.urls.static import static
from comment.views import CommentViewSet

from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)

router = DefaultRouter()
router.register(r'article', views.ArticleViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'avater', views.AvatarViewSet)
router.register(r'comment', CommentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    # drf 自动注册路由
    path('api/', include(router.urls)),
    ### TOKEN GET AND REFRESH
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh")
]
# http post http://127.0.0.1:8000/api/token/ username=will password=123

# 把媒体文件的路由注册了
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)