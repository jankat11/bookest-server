from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    google_id = models.CharField(max_length=20)
    no_cover = models.BooleanField(False)

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    _id = models.CharField(max_length=200)
    content = models.TextField(max_length=2500)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    on_book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="reviews")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.content

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "owner": self.owner.username,
            "on_book": self.on_book.google_id,
            "book": self.on_book.title,
            "time": self.time.strftime("%b %d %Y, %H:%M")
        }


class BookShelf(models.Model):
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="book_shelf")
    will_be_read = models.ManyToManyField(
        Book, blank=True, related_name="as_will_be_read", through="OrderWillBeRead")
    has_been_read = models.ManyToManyField(
        Book, blank=True, related_name="as_has_been_read", through="OrderHasBeenRead")

    def __str__(self) -> str:
        return f"{self.owner.username}'s bookshelf"

    def iterable(self):
        return {"will_be_read": self.will_be_read, "has_been_read": self.has_been_read}


class OrderWillBeRead(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookshelf = models.ForeignKey(BookShelf, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.bookshelf.owner} add {self.book} on {self.date_time}"


class OrderHasBeenRead(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookshelf = models.ForeignKey(BookShelf, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.bookshelf.owner} add {self.book} on {self.date_time}"
