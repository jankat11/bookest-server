from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from .models import Book, BookShelf
from rest_framework import status
from .serializers import *
from .helpers import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        print(serializer.items())
        for key, value in serializer.items():
            data[key] = value
        return data


class MyToken(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def register(request):
    if request.method == "POST":    
        data = request.data
        try:
            user = User.objects.create(
                username=data["email"],
                email=data["email"],
                password=make_password(data["password"])
            )
            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except:
            message = {"detail": "User with this email already exists"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def add_book(request):
    if request.method == "POST":
        data = get_book_credentials(request.data)
        book, _ = Book.objects.get_or_create(google_id=data["id"], isbn=data["isbn"], title=data["title"], no_cover=data["cover"])
        book_shelf, _ = BookShelf.objects.get_or_create(owner=request.user)
        try:
            check = book_shelf.iterable()[data["shelf"]].get(id=book.id)
            if check is not None:
                message = {"detail": f"This book is already in {data['shelf']} shelf"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        try:
            check = book_shelf.iterable()[data["other_shelf"]].get(id=book.id)
            if check is not None:
                book_shelf.iterable()[data["other_shelf"]].remove(book)
                book_shelf.save()
        except:
            pass
        book_shelf.iterable()[data["shelf"]].add(book)
        book_shelf.save()
        serialized = book_serializer(book_shelf)
        return JsonResponse(serialized)
      

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_books(request):
    try:
        book_shelf, _ = BookShelf.objects.get_or_create(owner=request.user)
        serialized = book_serializer(book_shelf)
        return JsonResponse(serialized)
    except:
      return JsonResponse({
          "sorry": "unsuccessful"
      })
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def remove_from_bookshelf(request, book_id):
    book_shelf = BookShelf.objects.get(owner=request.user)
    book = Book.objects.get(pk=book_id)
    try:
        book_shelf.will_be_read.remove(book)
    except:
        pass
    try:
        book_shelf.has_been_read.remove(book)
    except:
        pass
    return JsonResponse({
        "success": "the book removed successfully"
    })