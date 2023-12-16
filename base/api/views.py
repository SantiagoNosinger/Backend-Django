from django.http import JsonResponse
from ..models import Post, Comment, Like
from django.shortcuts import get_object_or_404


def routes(request):
    routes = [
        'GET / api/posts',
        'GET/ api/post/:id',
        'GET/ api/comment',
    ]

    return JsonResponse(routes,safe=False)

def post(request, id):
    post=Post.objects.get(id=id)
    posts_dict = {
        'title': post.title,
        'general':post.general,
        'text':post.text,
        'id':id
    }
    return JsonResponse(posts_dict, safe=False)


def posts(request):
    posts=Post.objects.all()
    posts_dict = []
    for p in posts:
        posts_dict.append({
            'title': p.title,
            'general':p.general,
            'text': p.text,
            
        })
    return JsonResponse(posts_dict, safe=False)


def comment(request, id):      
    comments = Comment.objects.all()
    comments_dict=[]
    for p in comments:
        comments_dict = [
            {

                'text': p.text,
                'user': p.user.username,
                
            }
            for comment in comments
        ]
    return JsonResponse(comments_dict, safe=False)



    
def likes(request, id):
    if request.method == 'GET':
        post_likes = Like.objects.all()
        likes_dict = []
        for p in post_likes:
            likes_dict = [
                {
                    'user': p.user.username,
                    
                }
                for like in post_likes
            ]
        return JsonResponse(likes_dict, safe=False)