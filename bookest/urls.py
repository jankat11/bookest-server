from django.urls import path
from . import views


urlpatterns = [
    path('users/login/', views.MyToken.as_view()),
    path('users/register/', views.register ),
    path('users/mybooks/', views.my_books ),
    path("users/addbook/", views.add_book ),
    path("removeBook/<str:book_id>", views.remove_from_bookshelf),
]
