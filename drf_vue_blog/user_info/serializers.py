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
        
# 注意 def update(...) 时，密码需要单独拿出来通过 set_password() 方法加密后存入数据库，而不能以明文的形式保存。
# 超链接字段的参数有一条 lookup_field，这是指定了解析超链接关系的字段。直观来说，将其配置为 username 后，
# 用户详情接口的地址表示为用户名而不是主键。        
        
class UserRegisterSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='username')

    class Meta:
        model = User
        fields=[
            'url',
            'id',
            'username',
            'password',
        ]

        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)
