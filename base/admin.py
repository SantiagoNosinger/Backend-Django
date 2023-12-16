from django.contrib import admin

# Register your models here.
from .models import Post, Comment,Perfil,Seguidores, Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Perfil)
admin.site.register(Seguidores)
admin.site.register(Like)
