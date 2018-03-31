from django.contrib.auth.models import User
from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField(source='userinfo.role')
    blocked = serializers.ReadOnlyField(source='userinfo.blocked', read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'role',
            'first_name',
            'last_name',
            'email',
            'blocked',
        )
