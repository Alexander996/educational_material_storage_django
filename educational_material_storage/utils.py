from django.db import transaction
from django.db.models import Q
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


def validate_request(data, *args):
    errors = {}
    msg = 'This field is required'
    for item in args:
        if data.get(item) is None:
            errors[item] = msg

    if errors:
        raise ValidationError(errors)


def paginate(paginator, serializer, queryset, request):
    paginator = paginator()
    context = paginator.paginate_queryset(queryset, request)
    serializer = serializer(context, many=True)
    return paginator.get_paginated_response(serializer.data)


def filter_by_category(request):
    q = Q()
    categories = request.GET.getlist('category')
    if categories is not None:
        for category in categories:
            q |= Q(categories__id=category)
    return q
