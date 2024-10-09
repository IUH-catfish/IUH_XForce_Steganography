from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Post

# posts = [
#     {
#         'author' : 'Me',
#         'title' : "About my block",
#         'content' : 'First Post',
#         'date_posted' : 'August 28, 2018',
#     },
#     {
#         'author' : 'Me Again',
#         'title' : "About my block num 2",
#         'content' : 'Second Post',
#         'date_posted' : 'August 29, 2018',
#     }
# ] 

def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    
    return render(request, 'blog/home.html', context)

def about(request):
    respond = '<h1>About This Blog Here</h1>'
    return render(request, 'blog/about.html', {'title':"about the page"})

def steganography(request):
    return render(request, 'blog/steganography.html', {'title':"about the page"})

