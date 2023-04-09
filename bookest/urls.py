from django.urls import path
from . import views


urlpatterns = [
    path('users/login/', views.MyToken.as_view()),
    path('users/register/', views.register),
    path('users/mybooks/', views.my_books),
    path("users/addbook/", views.add_book),
    path("users/removeBook/<str:book_id>", views.remove_from_bookshelf),
    path("users/addreview/", views.add_review),
    path("users/myreviews/", views.my_reviews),
    path("users/deletereview/<str:review_id>", views.delete_review),
]
