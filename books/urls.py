from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books.views import CategoryViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, base_name='category')

urlpatterns = [
    path('', include(router.urls)),
]
