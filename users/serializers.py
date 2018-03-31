from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import UserInfo


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    role = serializers.IntegerField(source='userinfo.role')
    blocked = serializers.ReadOnlyField(source='userinfo.blocked', read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'role',
            'first_name',
            'last_name',
            'email',
            'blocked',
        )

    def create(self, validated_data):
        user_info = validated_data.pop('userinfo')
        password = validated_data.pop('password')
        user = User.objects.create(password=make_password(password), **validated_data)
        UserInfo.objects.create(user=user, **user_info)
        return user
