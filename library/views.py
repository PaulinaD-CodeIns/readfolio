from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from django.contrib.auth.decorators import login_required

@login_required
def book_list(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'library/book_list.html', {'books': books})

@login_required
def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        status = request.POST.get('status')
        if title and author:
            Book.objects.create(
                title=title,
                author=author,
                status=status,
                user=request.user
            )
            return redirect('book_list')
    return render(request, 'library/book_form.html')

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    return render(request, 'library/book_detail.html', {'book': book})
