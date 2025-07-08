from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Review


# Book CRUD, list, and details

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
        if title and author and status:
            Book.objects.create(title=title, author=author, status=status, user=request.user)
            return redirect('book_list')
    return render(request, 'library/book_form.html')

@login_required
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk, user=request.user)
    except Book.DoesNotExist:
        return redirect('book_list')

    return render(request, 'library/book_detail.html', {'book': book})

@login_required
def book_update(request, pk):
    book = Book.objects.get(pk=pk, user=request.user)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.status = request.POST.get('status')
        book.save()
        return redirect('book_list')

    return render(request, 'library/book_form.html', {'book': book})

@login_required
def book_delete(request, pk):
    book = Book.objects.get(pk=pk, user=request.user)

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'library/book_confirm_delete.html', {'book': book})


# Review CRUD, list and detail

@login_required
def review_list(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'library/review_list.html', {'reviews': reviews})
