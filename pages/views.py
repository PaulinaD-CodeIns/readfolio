from django.shortcuts import render
from library.models import Review


# Home page blog of reviews
def home(request):
    public_reviews = Review.objects.filter(is_public=True).select_related('book').order_by('?')[:5]
    return render(request, 'pages/home.html', {'public_reviews': public_reviews})





# About us page
def about(request):
    return render(request, 'pages/about.html')