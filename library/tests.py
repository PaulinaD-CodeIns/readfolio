from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Book, Review
from .forms import ReviewForm


# ------------------ MODEL TESTS ------------------

class BookModelTest(TestCase):
    def test_string_representation(self):
        book = Book(title="1984", author="George Orwell")
        self.assertEqual(str(book), "1984")

    def test_book_creation(self):
        user = User.objects.create_user(username='testuser', password='pass1234')
        book = Book.objects.create(title="Test Book", author="Author A", status="To Read", user=user)
        self.assertEqual(book.status, "To Read")
        self.assertEqual(book.user.username, 'testuser')


class ReviewModelTest(TestCase):
    def test_review_string(self):
        user = User.objects.create_user(username='reviewer', password='pass1234')
        book = Book.objects.create(title="Review Book", author="Author B", status="Finished", user=user)
        review = Review.objects.create(book=book, rating=4, content="Great read!", is_public=True, user=user)
        self.assertIn("Review Book", str(review))


# ------------------ VIEW TESTS ------------------

class BookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.book = Book.objects.create(user=self.user, title="The Hobbit", author="J.R.R. Tolkien", status="To Read")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('book_list'))
        self.assertRedirects(response, '/accounts/login/?next=/books/')

    def test_logged_in_user_can_see_books(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Hobbit")

    def test_create_book_view(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(reverse('book_create'), {
            'title': 'New Book',
            'author': 'Author C',
            'status': 'reading'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title='New Book').exists())


# ------------------ FORM TESTS ------------------

class ReviewFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='formuser', password='pass1234')
        self.book = Book.objects.create(user=self.user, title="Form Book", author="Author D", status="Finished")

    def test_invalid_review_missing_rating(self):
        """Form should be invalid if rating is missing"""
        form_data = {
            'content': 'Interesting read',
            'is_public': True
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        self.assertEqual(form.errors['rating'], ['This field is required.'])

    def test_valid_review_submission(self):
        self.client.login(username='formuser', password='pass1234')
        response = self.client.post(reverse('create_review', args=[self.book.pk]), {
            'rating': 5,
            'content': 'Loved it!',
            'is_public': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(book=self.book, rating=5).exists())
