import json

from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from books.models import Category, Book
from books.serializers import CategorySerializer, BookSerializer
from educational_material_storage.utils import validate_request, transaction_atomic, paginate, filter_by_category
from users.models import UserBook


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

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


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        if self.action == 'list':
            q = filter_by_category(self.request)
            q &= Q(deleted=False)
            return Book.objects.filter(q).distinct()
        else:
            return Book.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @transaction_atomic
    def create(self, request, *args, **kwargs):
        if request.content_type == 'application/json':
            raise ValidationError('Use "multipart/form-data", not "application/json"')

        data = request.data
        validate_request(data, 'file', 'author', 'name', 'categories')
        json_data = {}

        file = data.pop('file')[0]
        categories = json.JSONDecoder().decode(data.pop('categories')[0])
        json_data['categories'] = categories

        for attr, value in data.items():
            json_data[attr] = value

        serializer = self.get_serializer(data=json_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user, file=file)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        book.deleted = True
        book.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'], url_path='take')
    @transaction_atomic
    def take_book(self, request, pk=None):
        book = self.get_object()
        UserBook.objects.create(book=book, user=request.user.userinfo)
        return Response()

    @detail_route(methods=['post'], url_path='remove')
    @transaction_atomic
    def remove_book(self, request, pk=None):
        book = self.get_object()
        try:
            user_book = UserBook.objects.get(book=book, user=request.user.userinfo)
        except UserBook.DoesNotExist:
            raise ValidationError('You have not this book')
        user_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(url_path='search')
    def book_search(self, request):
        text = request.GET.get('text')
        if text is None:
            raise ValidationError(dict(detail='Field "text" is empty'))

        q = (Q(name__icontains=text) |
             Q(author__icontains=text) |
             Q(categories__name__icontains=text))

        q &= Q(deleted=False)
        books = Book.objects.filter(q).distinct()
        return paginate(PageNumberPagination, BookSerializer, books, request)
