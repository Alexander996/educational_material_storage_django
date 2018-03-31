from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books.views import CategoryViewSet, BookViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, base_name='category')
router.register('books', BookViewSet, base_name='book')

urlpatterns = [
    path('', include(router.urls)),
]
