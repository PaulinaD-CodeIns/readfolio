from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Book, Review
from .forms import ReviewForm, BookForm


# Book CRUD, list, and details 


# Book List
@login_required
def book_list(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'library/book_list.html', {'books': books})


# Book CRUD: Create
@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form})

# Book CRUD: Read
@login_required
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk, user=request.user)
    except Book.DoesNotExist:
        return redirect('book_list')

    return render(request, 'library/book_detail.html', {'book': book})

# Book CRUD: Update
@login_required

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'library/book_form.html', {'form': form})

# Book CRUD: Delete
@login_required
def book_delete(request, pk):
    book = Book.objects.get(pk=pk, user=request.user)

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'library/book_confirm_delete.html', {'book': book})


# Review CRUD, list and detail


# Review List
@login_required
def review_list(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'library/review_list.html', {'reviews': reviews})


# Review CRUD: Create
@login_required
def create_review(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_list')
    else:
        form = ReviewForm()

    return render(request, 'library/review_form.html', {'form': form, 'book': book})


# Review CRUD: Read
@login_required
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if not review.is_public and review.user != request.user:
        return redirect('review_list')

    return render(request, 'library/review_detail.html', {'review': review})


# Review CRUD: Update
@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this review.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_detail', pk=review.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'library/review_form.html', {'form': form, 'book': review.book})


# Review CRUD: Delete
@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    if request.method == 'POST':
        review.delete()
        return redirect('review_list')

    return render(request, 'library/review_confirm_delete.html', {'review': review})