from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from .serializers import *
from .models import *
from .helpers import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
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
        book, _ = Book.objects.get_or_create(
            google_id=data["id"], isbn=data["isbn"], title=data["title"], no_cover=data["cover"])
        book_shelf, _ = BookShelf.objects.get_or_create(owner=request.user)
        try:
            check = book_shelf.serialize()[data["shelf"]].get(id=book.id)
            if check is not None:
                message = {
                    "detail": f"This book is already in {data['shelf']} shelf"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        try:
            check = book_shelf.serialize()[data["other_shelf"]].get(id=book.id)
            if check is not None:
                book_shelf.serialize()[data["other_shelf"]].remove(book)
                book_shelf.save()
        except:
            pass
        book_shelf.serialize()[data["shelf"]].add(book)
        book_shelf.save()
        serialized = book_serializer(book_shelf)
        return JsonResponse(serialized)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_books(request):
    try:
        book_shelf, _ = BookShelf.objects.get_or_create(owner=request.user)
        serialized = book_serializer(book_shelf)
        users_reviews = request.user.reviews.all()
        noted_books = [review.on_book.serialize() for review in users_reviews]
        return JsonResponse({
          "mainShelf":  serialized,
          "noted_books": noted_books
        })
    except:
        return JsonResponse({
            "sorry": "unsuccessful",
            
        })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def remove_from_bookshelf(request, book_id):
    book_shelf = BookShelf.objects.get(owner=request.user)
    book = Book.objects.get(google_id=book_id)
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def my_reviews(request):
    if request.method == "POST":
        try:
            user = request.user
            data = get_book_on_notes(request.data)
            book, _ = Book.objects.get_or_create(
                google_id=data["id"], isbn=data["isbn"], title=data["title"], no_cover=data["cover"])
            reviews = Review.objects.all().filter(owner=user, on_book=book)
            reviews_sorted = sorted(reviews,
                                    key=lambda review: review.time, reverse=True)
            reviews_serialized = [review.serialize() for review in reviews_sorted]
            return JsonResponse({
                "reviews": reviews_serialized
            })
        except:
            message = {"detail": "could not get notes:("}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request):
    if request.method == "POST":
        try:
            user = request.user
            data = get_review_credentials(request.data)
            book, _ = Book.objects.get_or_create(
                google_id=data["id"], isbn=data["isbn"], title=data["title"], no_cover=data["cover"])
            content = data["content"].replace("\n", "<br>")
            _id = data["_id"]
            Review.objects.create(owner=user, on_book=book, content=content, _id=_id)
            return JsonResponse({
                "result":  "your note was successfully added"
            })
        except:
            message = {"detail": "something went wrong:( try later"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_review(request):
    if request.method == "POST":
        try:
            note_id = request.data["noteId"]
            review = Review.objects.get(_id=note_id, owner=request.user)
            review.delete()
            return JsonResponse({
                "success": "the note deleted successfully"
            })
        except: 
            message = {"detail": "something went wrong:( try later"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
