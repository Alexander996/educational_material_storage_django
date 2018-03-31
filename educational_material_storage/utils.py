from django.db import transaction
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet


class CRUModelViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """
    ModelViewSet without DELETE.
    """
    pass


def transaction_atomic(func):
    def inner(*args, **kwargs):
        try:
            with transaction.atomic():
                return func(*args, **kwargs)
        except Exception as e:
            raise ValidationError(dict(exception=e.__class__.__name__, detail=e))

    return inner
