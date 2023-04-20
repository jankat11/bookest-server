from django.urls import path
from . import views


urlpatterns = [
    path('users/login/', views.MyToken.as_view(), name="login"),
    path('users/register/', views.register, name="register"),
    path('users/mybooks/', views.my_books),
    path("users/addbook/", views.add_book),
    path("users/removeBook/<str:book_id>", views.remove_from_bookshelf),
    path("users/addreview/", views.add_review),
    path("users/myreviews/", views.my_reviews),
    path("users/deletenote/", views.delete_review),
    path('auth/google/callback/', views.google_callback),
    path('users/getbooks/<str:genre>', views.get_books),
]
