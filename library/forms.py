from django import forms
from .models import Review, Book

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating', 'is_public']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 10,
                'style': 'width: 100%; font-size: 1rem; padding: 1rem; border-radius: 8px;',
                'required': True,
                'placeholder': 'Write your review here...'
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'required': True,
                'class': 'form-control',
            }),
            'is_public': forms.CheckboxInput(attrs={
                'aria-label': 'Make this review public',
                'class': 'form-check-input',
            }),
        }

        
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

