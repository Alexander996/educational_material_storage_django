from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.TextField(max_length=150)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']


class Book(models.Model):
    auto_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.TextField(max_length=250)
    author = models.TextField(max_length=150)
    file = models.FileField(upload_to='materials/%Y/%m/%d/')
    categories = models.ManyToManyField(Category, through='CategoryBook')
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-auto_date']


class CategoryBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('book', 'category')
