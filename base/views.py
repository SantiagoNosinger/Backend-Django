from django.urls import reverse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post, Comment, Perfil, Seguidores, Like
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def loginPage(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Se inicio sesión.")
                return redirect('/')
            
        messages.error(request, "Usuario o contraseña incorrectas.")
            
    return render(request, 'login.html')

def logoutPage(request):
    logout(request)
    return redirect('/')

def registro(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if (password != confirm_password):
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('/registro')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ya existe ese usuario')
            return redirect('/registro')    
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe ese enail.')
            return redirect('/registro')
        User.objects.create_user(username, email=email, password=password)
        return redirect('/login')
    return render(request,'registros.html') 

def home(request):  
    posts= Post.objects.all()
    return render(request, 'home.html', {'posts':posts})


def post(request, id=None):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id is None:
            Post.objects.create(
                title=request.POST.get('title'),
                general=request.POST.get('general'),
                text=request.POST.get('text'),
                user=request.user 
            )
        else:
            p = Post.objects.get(id=id)
            if p.user == request.user:
                p.title = request.POST.get('title')
                p.general=request.POST.get('general')
                p.text = request.POST.get('text')
                p.save()
        
    context = {}
    if id is not None:
        p = Post.objects.get(id=id)
        context['post'] = p

    return render(request, 'post.html', context)

def comment(request):
    p = Post.objects.get(id=request.POST.get('post'))
    Comment.objects.create(
        text=request.POST.get('text'),
        user=request.user,
        post = p
    )
    return redirect('paginapost', id=p.id)



def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user == post.user:
        post.delete()

    return redirect('home')

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user == comment.user:
        comment.delete()   
    return redirect('paginapost', id=comment.post.id)


def paginapost(request, id):
    post = get_object_or_404(Post, id=id)
    context = {'post': post}
    return render(request, 'paginapost.html', context)


def perfil(request, username):
    user = User.objects.get(username=username)
    perfil, creado = Perfil.objects.get_or_create(user=user)
    
    posts = Post.objects.filter(user=user)
    sugerencia = perfil.sugerencias_seguir()
    context = {'user': user, 'posts': posts, 'sugerencia': sugerencia}
    return render(request, 'perfil.html', context)

@login_required
def editar_perfil(request):
    usuario = request.user
    perfil, creado = Perfil.objects.get_or_create(user=usuario)

    if request.method == 'POST':
        bio_nueva = request.POST.get('bio')
        imagen_nueva = request.FILES.get('image')

        
        perfil.bio = bio_nueva
        if imagen_nueva:
            perfil.image = imagen_nueva
        perfil.save()

        return redirect('perfil', username=usuario.username)

    return render(request, 'editarperfil.html', {'perfil': perfil})

@login_required
def follow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Seguidores(from_user=current_user, to_user=to_user_id)
	rel.save()
	return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Seguidores.objects.get(from_user=current_user.id, to_user=to_user_id)
	rel.delete()
	return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def like(request, id):
    user = request.user
    post = Post.objects.get(id=id)
    current_like = post.likes
    liked= Like.objects.filter(user=user, post=post).count()

    if not liked:
        Like.objects.create(user=user, post=post)
        current_like=current_like + 1
    else:
        Like.objects.filter(user=user, post=post).delete()
        current_like=current_like - 1

    post.likes=current_like
    post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('paginapost', args=[id])))

def likes_modal(request, post_id):
    post = Post.objects.get(id=post_id)
    likes_users = post.get_likes_users()
    return render(request, 'likes_modal.html', {'likes_users': likes_users})

@login_required
def sugerencias_seguir(request):
    perfil_actual = request.user.perfil
    sugerencias = perfil_actual.sugerencias_seguir()
    context = {'sugerencias': sugerencias}
    return redirect(request.META.get('HTTP_REFERER', 'home'), context)
