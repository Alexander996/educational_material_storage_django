from rest_framework import viewsets, status
from rest_framework.response import Response

from books.models import Category
from books.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(deleted=False)
        else:
            return Category.objects.all()

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        category.deleted = True
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
