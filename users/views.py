from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from educational_material_storage.utils import CRUModelViewSet, transaction_atomic
from users.serializers import UserSerializer


class UserViewSet(CRUModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        else:
            return super().get_permissions()

    @transaction_atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = get_object_or_404(User, pk=serializer.data['id'])
        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        data = dict(token=token.key, **serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
