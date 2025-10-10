from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/vote/', views.vote, name='vote'),
    path('create/', views.create_post, name='create_post'),
]