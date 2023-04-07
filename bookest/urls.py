from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('users/login/', views.MyToken.as_view(), name='token_obtain_pair'),
    path('users/register/', views.register, name='register'),
    path('users/mybooks/', views.my_books, name='my_books'),
    path("users/addbook/", views.add_book, name="addbook"),
]
