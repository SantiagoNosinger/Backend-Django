from django.db import models

from django.contrib.auth.models import User


class Post(models.Model):
    
    title = models.CharField(max_length = 200)
    general = models.CharField(max_length = 200)
    text= models.TextField() 
    update = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title 
    
    class Meta:
        ordering = ['-created']
    
    def get_likes_users(self):
        return self.post_like.values_list('user__username', flat=True)

    
    
class Comment(models.Model):
    text= models.TextField() 
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    


class Perfil(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    bio = models.CharField(default='Hola!!', max_length=100)
    image = models.ImageField()

    def __str__(self):
        return  f'Perfil de {self.user.username}'
    
    def following(self):
        user_ids=Seguidores.objects.filter(from_user=self.user)\
                                .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def  followers(self):   
        user_ids=Seguidores.objects.filter(to_user=self.user)\
                                .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)
    
    def sugerencias_seguir(self):
        users_to_follow = User.objects.exclude(id__in=self.following()).exclude(id=self.user.id).exclude(id__in=self.followers())
        return users_to_follow
    
    def get_likes_users(self):
        return self.post_like.values_list('user__username', flat=True)
    
class Seguidores(models.Model):
    from_user = models.ForeignKey(User, related_name='seguidores', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='seguimiento', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

    

