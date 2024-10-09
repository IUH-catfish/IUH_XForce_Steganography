from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.steganography, name = 'blog-steg'),
    path('home/', views.home, name = 'blog-home'),
    path('about/', views.about, name = 'blog-about'),
]