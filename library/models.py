from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Book Model -- 
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.author}"



# Review Model --

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return f"Review of '{self.book.title}' by {self.user.username}"
