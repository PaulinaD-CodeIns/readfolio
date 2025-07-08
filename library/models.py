from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Book Model -- 
class Book(models.Model):
    STATUS_CHOICES = [
        ('to_read', 'To Read'),
        ('reading', 'Reading'),
        ('finished', 'Finished'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_read')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



# Review Model --

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return f"Review of '{self.book.title}' by {self.user.username}"
