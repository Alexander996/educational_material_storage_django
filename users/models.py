from django.contrib.auth.models import User
from django.db import models

from books.models import Book


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    role = models.IntegerField()
    blocked = models.BooleanField(default=False)
    books = models.ManyToManyField(Book, through='UserBook')


class UserBook(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('user', 'book')
