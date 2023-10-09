from django.urls import path
from article import views

app_name = 'article'

urlpatterns = [
    ## as_view() 當其為類時所使用
    path('', views.article_list.as_view(), name='list'),
    path('<int:pk>/', views.ArticleDetail.as_view(), name='detail'),
]