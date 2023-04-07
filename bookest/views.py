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


@api_view(["GET"])
def index(request):
    print("user is: ", request.user)
    return Response({"message": "Hello, world!"})


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
      google_id = request.data["googleId"]
      isbn = request.data["isbn"]
      title = request.data["title"]
      no_cover = request.data["noCover"]
      will_be_read = request.data["willBeRead"]
      has_been_read = request.data["hasBeenRead"]
      if Book.objects.filter(google_id=google_id).all().count() == 0:
          Book.objects.create(google_id=google_id, isbn=isbn,
                              title=title, no_cover=no_cover)
      if BookShelf.objects.filter(owner=request.user).all().count() == 0:
          BookShelf.objects.create(owner=request.user)
      book = Book.objects.get(google_id=google_id)
      book_shelf = BookShelf.objects.get(owner=request.user)

      if will_be_read:
          try:
              check = book_shelf.will_be_read.get(id=book.id)
              if check is not None:
                message = {"detail": "This book is already in 'will be read' shelf"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
          except:
              pass
          try:
              check = book_shelf.has_been_read.get(id=book.id)
              if check is not None:
                  book_shelf.has_been_read.remove(book)
                  book_shelf.save()
          except:
              pass
          book_shelf.will_be_read.add(book)
          book_shelf.save()
          serialized = book_serializer(book_shelf)
          return JsonResponse(serialized)
      elif has_been_read:
          try:
              check = book_shelf.has_been_read.get(id=book.id)
              if check is not None:
                  message = {"detail": "This book is already in 'has been read' shelf"}
                  return Response(message, status=status.HTTP_400_BAD_REQUEST)
          except:
              pass
          try:
              check = book_shelf.will_be_read.get(id=book.id)
              if check is not None:
                  book_shelf.will_be_read.remove(book)
                  book_shelf.save()
          except:
              pass
          book_shelf.has_been_read.add(book)
          book_shelf.save()
          serialized = book_serializer(book_shelf)
          return JsonResponse(serialized)
    elif request.method == "GET":
      return JsonResponse({
          "hello": "world"
      })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_books(request):
    try:
        book_shelf = BookShelf.objects.get(owner=request.user)
        serialized = book_serializer(book_shelf)
        return JsonResponse(serialized)
    except:
      return JsonResponse({
          "sorry": "unsuccessful"
      })