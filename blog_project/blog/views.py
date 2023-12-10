from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm


def search_results(request):
    query = request.GET.get('query')
    
    # Debugging statement
    print(f"Query: {query}")

    if query:
        # Debugging statement
        print("Performing search...")
        
        # Perform a case-insensitive search by title
        results = BlogPost.objects.filter(title__icontains=query).order_by('-created_at')

        # Debugging statement
        print(f"Results: {results}")
    else:
        results = []

    return render(request, 'search_results.html', {'results': results, 'query': query})

@login_required(login_url='login')
def read_more(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('read_more', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'read_more.html', {'post': post, 'comments': comments, 'form': form})

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)  # Pass request.FILES for image upload
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('dashboard')
    else:
        form = BlogPostForm()

    return render(request, 'create_post.html', {'form': form})

def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})

def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    post.delete()
    return redirect('dashboard')

def dashboard(request):
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'dashboard.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login') 
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard') 
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    posts = BlogPost.objects.all()
    return render(request, 'index.html', {'posts': posts})
