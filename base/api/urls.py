
from django.urls import path
from .import views

urlpatterns = [
    path('', views.routes),
    path('posts/', views.posts),
    path('post/<int:id>', views.post),
    path('post/<int:id>/comment', views.comment),
    path('post/<int:id>/likes', views.likes)
]

    