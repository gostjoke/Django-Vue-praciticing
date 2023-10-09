from django.contrib.auth.models import User
from rest_framework import serializers

class UserDescSerializer(serializers.ModelSerializer):
    """ 於文章列表中引用的嵌套列化器 """

    class Meta:
        model = User
        fields = ['id', 
                  'username', 
                  'last_login',
                  'date_joined']