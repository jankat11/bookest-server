from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Book, BookShelf


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', "token"]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


def book_serializer(book_shelf):
    return    {     
        "will_be_read" : [{"id": book.book.google_id, "cover": book.book.no_cover, "title": book.book.title[0:10]}
                        for book in book_shelf.orderwillberead_set.all().order_by("date_time")],
        "has_been_read" : [{"id": book.book.google_id, "cover": book.book.no_cover, "title": book.book.title[0:10]}
                         for book in book_shelf.orderhasbeenread_set.all().order_by("date_time")]
    }
    