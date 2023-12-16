from django.urls import path 
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post), #
    path('post/<int:id>', views.post),
    path('login/', views.loginPage),
    path('logout/', views.logoutPage),
    path('registro/',views.registro),
    path('comment/', views.comment),
    path('pagina/<int:id>', views.paginapost, name='paginapost'),
    path('delete_post/<int:id>', views.delete_post, name='delete_post'),
    path('perfil/<str:username>/', views.perfil, name='perfil'),
    path('editar', views.editar_perfil, name='editar'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('like/<int:id>', views.like, name='like'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)