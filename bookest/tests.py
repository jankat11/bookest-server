from django.test import TestCase, Client
from .models import Book, BookShelf, Review
from django.contrib.auth.models import User
from django.urls import reverse
from string import ascii_lowercase
# Create your tests here.


class BookestTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        reader = User.objects.create(username="randomOsman", password="1234")
        book1 = Book.objects.create(
            isbn="mydummyisbn1", title="an example book1", google_id="randomgoogleid1", no_cover=False)
        book2 = Book.objects.create(
            isbn="mydummyisbn2", title="an example book2", google_id="randomgoogleid2", no_cover=False)

        bookshelf = BookShelf.objects.create(owner=reader)
        bookshelf.will_be_read.add(book1)
        bookshelf.has_been_read.add(book2)

        Review.objects.create(
            owner=reader, _id="1234", on_book=book1, content=ascii_lowercase*50)
        
        Review.objects.create(
            owner=reader, _id="5678", on_book=book2, content=ascii_lowercase*100)
        

    def test_user_model_exists(self):
        user = User.objects.get(username="randomOsman")
        self.assertEqual(user.username, "randomOsman")

    def test_book_model_exists(self):
        books = Book.objects.all()
        self.assertEqual(books.count(), 2)

    def test_user_has_bookshelf(self):
        user = User.objects.get(username="randomOsman")
        self.assertEqual(user.book_shelf, BookShelf.objects.get(owner=user))

    def test_is_valid_review(self): 
        review = Review.objects.get(_id="1234")
        self.assertTrue(review.is_valid())

    def test_is_invalid_review(self): 
        review = Review.objects.get(_id="5678")
        self.assertFalse(review.is_valid())

    def test_is_wrong_login_method(self):
        response = self.client.get("/api/users/login/")
        self.assertEqual(response.status_code, 405)

    def test_is_wrong_register_method(self):
        response = self.client.get("/api/users/register/")
        self.assertEqual(response.status_code, 405)

    def test_is_register_new_user(self):
        url = reverse("register")
        userdata = {"username": "randomUser", "password": "12345"}
        response = self.client.post(url, userdata)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_is_register_existing_user(self):
        url = reverse("register")
        userdata = {"username": "randomOsman", "password": "12345"}
        response = self.client.post(url, userdata)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

