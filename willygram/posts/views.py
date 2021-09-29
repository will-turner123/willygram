from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
# Create your views here.
from .models import Post, PostLikes, PostComment
from .forms import PostCreateForm
from users.models import UserFollowing
from itertools import chain
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
from datetime import datetime, timedelta

# TODO: add in handling for posts not found & users not found in user views


def all_posts(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'posts/home.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed')
        else:
            print(form.errors)
    else:
        form = PostCreateForm()
    return render(request, 'posts/post_form.html', {'form': form, 'title': 'New Post'})



def get_like_amount(post=1):
    count = PostLikes.objects.filter(post_id=post).count()
    return count

def has_liked_post(user, post):
    return PostLikes.objects.filter(post_id=post, liked_by=user).exists()

def get_comment_amount(post=1):
    count = PostComment.objects.filter(post_id=post).count()
    return count

def get_comments(post=1):
    comments = PostComment.objects.filter(post_id=post)
    return comments



@login_required
def feed(request):
    following = UserFollowing.objects.filter(user_id=request.user)
    post_list = []
    for user in following:
        user = user.following_user_id
        for post in Post.objects.filter(author=user).order_by('-pk'):
            post_list.append(post)
    post_dict = {}
    post_list = list(sorted(post_list, key=lambda k: k.pk, reverse=True))
    for post in post_list:
        post_dict[post.pk] = {'likes': get_like_amount(post=post), 'post': post, 'has_liked': has_liked_post(request.user, post), 
        'username': post.author.username, 'comment_count': get_comment_amount(post),
        'comments': get_comments(post)}
    # print(post_dict)
    # post_dict = sorted(post_dict.items(), key=lambda i: i[1]['post'].pk)
    # post_dict = {int(k) : v for k, v in post_dict.items()}
    return render(request, 'posts/feed.html', {'posts': post_dict, 'title': 'Your Feed'})
    

@login_required
def explore(request):
    post_dict = {}
    for post in Post.objects.all().order_by('-id')[:100]:
        post_dict[post.pk] = {'likes': get_like_amount(post=post), 'post': post, 'has_liked': has_liked_post(request.user, post), 
        'username': post.author.username, 'comment_count': get_comment_amount(post),
        'comments': get_comments(post)}
    # explore algorithm: 
    # ((likes*like_weight) + (comments*comment_weight)-(days_ago*days_ago_weight))
    like_weight = 1
    comment_weight = 2
    days_ago_weight = 2
    now = datetime.now()
    post_dict = {k: v for k, v in sorted(post_dict.items(), key=lambda item: (((item[0]*like_weight) + (item[-2]*comment_weight))-(
        (timezone.now() - item[1]['post'].date_posted).days * days_ago_weight
    )
))}
    return render(request, 'posts/feed.html', {'posts': post_dict, 'title': 'Explore'})

def view_post(request, post=1):
    post_dict[post] = {'likes': get_like_amount(post=post), 'post': Post.objects.get(pk=post), 'has_liked': has_liked_post(request.user, post), 
        'username': post.author.username}
    return render(request, 'posts/view_post.html', {'post': post_dict, 'title': f'View {post.author.username}s post'})


def like_post(request):
    if request.is_ajax and request.method == "GET":
        post = request.GET.get("post")
        to_like = Post.objects.filter(pk=post)
        liked = False
        if to_like.exists():
            to_like = to_like.first()
            if has_liked_post(request.user, to_like) is False:
                PostLikes.objects.create(post_id=to_like, liked_by=request.user)
                liked = True
            else:
                PostLikes.objects.get(post_id=to_like, liked_by=request.user).delete()
                liked = False
            return JsonResponse({"valid": True, "liked": liked}, status=200)
        else:
            return JsonResponse({"valid": False, "liked": liked}, status = 200)
    return JsonResponse({}, status=400)


def create_comment(request):
    if request.is_ajax and request.method == "GET":
        post = request.GET.get("post")
        content = request.GET.get("content")
        to_comment = Post.objects.filter(pk=post)
        print('here1')
        if to_comment.exists():
            print('here2')
            to_comment = to_comment.first()
            PostComment.objects.create(post_id=to_comment, content=content, author=request.user)
            last_post = PostComment.objects.filter(post_id=to_comment, content=content, author=request.user).order_by('-id')[0].pk
            return JsonResponse({"valid": True, "commented": True, "id": last_post}, status=200)
        else:
            print('here3')
            return JsonResponse({"valid": False, "commented": False}, status=400)
    return JsonResponse({}, status=400)



def delete_comment(request):
    if request.is_ajax and request.method == "GET":
        comment = request.GET.get("comment")
        to_delete = PostComment.objects.filter(pk=comment)
        if to_delete.exists() and (to_delete.first().author == request.user or request.user.is_superuser):
            to_delete = to_delete.first()
            to_delete.delete()
            return JsonResponse({"valid": True, "deleted": True}, status=200)
        else:
            return JsonResponse({"valid": False, "deleted": False}, status=400)
    return JsonResponse({}, status=400)


def delete_post(request):
    if request.is_ajax and request.method == "GET":
        post = request.GET.get("post")
        to_delete = Post.objects.filter(pk=post)
        if to_delete.exists():
            to_delete = to_delete.first()
            if to_delete.author == request.user or request.user.is_superuser:
                to_delete.delete()
                return JsonResponse({"valid": True, "deleted": True}, status=200)
            else:
                return JsonResponse({"valid": False, "deleted": False}, status=401)
    return JsonResponse({}, status=400)



def view_post(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'posts/home.html', context)



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
