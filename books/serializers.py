from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.models import Category, Book, CategoryBook
from users.models import UserBook
from users.user_list_serializer import UserListSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('deleted',)


class CategoryBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryBook
        exclude = ('book',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['category'] = CategorySerializer().to_representation(instance.category)
        return ret


class BookSerializer(serializers.ModelSerializer):
    owner = UserListSerializer(read_only=True)
    categories = CategoryBookSerializer(source='categorybook_set', many=True)
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('deleted',)

    def create(self, validated_data):
        categories = validated_data.pop('categorybook_set')
        if not categories:
            raise ValidationError('"categories" can not be empty')

        book = Book.objects.create(**validated_data)
        UserBook.objects.create(book=book, user=self.context['request'].user.userinfo)
        for category in categories:
            CategoryBook.objects.create(book=book, **category)

        return book

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        categories = []
        for category in ret['categories']:
            categories.append(category['category'])
        ret['categories'] = categories
        return ret
