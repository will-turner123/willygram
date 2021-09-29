from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, UserFollowing
from posts.models import Post, PostLikes
from posts.views import (get_like_amount, has_liked_post, get_comment_amount, get_comments)

# Create your views here.
def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        if u_form.is_valid():
            user = u_form.save()
            user.profile.save()
            messages.success(request, f'Your account has been created!')
            return redirect('login')
    else:
        u_form = UserRegisterForm()
    return render(request, 'users/register.html', {'u_form': u_form, 'title': 'Register'})

 
def is_following(request, viewed_user):
    is_following = False
    if UserFollowing.objects.filter(user_id=viewed_user, following_user_id=request.user).exists():
        is_following = True
    print(f'{viewed_user.username} {is_following}  {request.user.username}')
    return is_following

def get_follower_count(user):
    return UserFollowing.objects.filter(user_id = user).count()

def get_following_count(user):
    return UserFollowing.objects.filter(following_user_id=user).count()

def get_followers(user, amount=4):
    return UserFollowing.objects.filter(user_id=user)[:amount]

def get_following(user, amount=4):
    return UserFollowing.objects.filter(following_user_id=user)[:amount]

def get_likes(user):
    like_count = 0
    for post in Post.objects.filter(author=user):
        like_count += PostLikes.objects.filter(post_id=post).count()
    return like_count


def view_followers(request, username='hello7'):
    get_user = User.objects.get(username=username)
    followers = get_followers(get_user, amount=100)
    follower_dict = {}
    for follower in followers:
        follower_dict[follower.pk] = {'follower': follower, 'is_following': is_following(request, follower.following_user_id)}
    return render(request, 'users/view_followers.html', {'followers': follower_dict.items(), 'queried_user': username,
    'title': f"{username}'s followers"})


def view_following(request, username='hello7'):
    get_user = User.objects.get(username=username)
    followers = get_following(get_user, amount=100)
    follower_dict = {}
    for follower in followers:
        follower_dict[follower.pk] = {'follower': follower, 'is_following': is_following(request, follower.user_id)}
    return render(request, 'users/view_following.html', {'followers': follower_dict.items(), 'queried_user': username,
    'title': f"{username}'s followings"})



@login_required
def view_profile(request, username='hello7'):
    viewed_user = User.objects.get(username=username)
    check_following = is_following(request, viewed_user)
    follower_count = get_follower_count(viewed_user)
    following_count = get_following_count(viewed_user)

    # COPY / PASTED from feed() in post views
    following = UserFollowing.objects.filter(user_id=viewed_user)
    post_list = Post.objects.filter(author=viewed_user).order_by('-pk')
    post_dict = {}
    for post in post_list:
        post_dict[post.pk] = {'likes': get_like_amount(post=post), 'post': post, 'has_liked': has_liked_post(request.user, post), 
        'username': post.author.username, 'comment_count': get_comment_amount(post),
        'comments': get_comments(post)}
    # end copy / paste
    return render(request, 'users/view_profile.html', {'viewed_user': viewed_user, 'is_following': check_following, 'follower_count': follower_count,
    'following_count': following_count, 'likes': get_likes(viewed_user), 'posts': post_dict, 'title': f"{viewed_user.username}'s profile"})


def follow(request):
    if request.is_ajax and request.method == "GET":
        follow_user = request.GET.get("user")
        to_follow = User.objects.filter(pk=follow_user)
        followed = False
        print(f'here0')
        if to_follow.exists():
            print(f'here')
            to_follow = to_follow.first()
            if UserFollowing.objects.filter(user_id=to_follow, following_user_id=request.user).exists() is False:
                print(f'here1')
                UserFollowing.objects.create(user_id=to_follow, following_user_id=request.user)
                followed = True
            elif to_follow != request.user:
                print(f'here2')
                UserFollowing.objects.get(user_id=to_follow, following_user_id=request.user).delete()
                followed = False
            return JsonResponse({"valid": True, "followed": followed}, status=200)
        else:
            return JsonResponse({"valid": False, "followed": followed}, status = 200)
    return JsonResponse({}, status=400)



# @login_required
# def follow(request, username='hello7'):
#     follow_user = User.objects.get(username=username)
#     if is_following(request, follow_user) is False:
#         UserFollowing.objects.create(user_id=follow_user,
#                                 following_user_id=request.user)
#     return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unfollow(request, username='hello7'):
    follow_user = User.objects.get(username=username)
    unfollow = UserFollowing.objects.get(user_id=follow_user, following_user_id=request.user)
    # UserFollowing.objects.delete(user_id=request.user, following_user_id=)
    unfollow.delete()
    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def profile_page(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user, current_user=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile,)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            email = u_form.cleaned_data.get('email')
            messages.success(request, f'Your profile has been updated!')
        u_form = UserUpdateForm(instance=request.user)
    u_form = UserUpdateForm(None, current_user=request.user, instance=request.user)
    p_form = ProfileUpdateForm(None, current_user=request.user, instance=request.user.profile)      
    follower_count = get_follower_count(request.user)
    following_count = get_following_count(request.user) 

    # COPY / PASTED from feed() in post views
    following = UserFollowing.objects.filter(user_id=request.user)
    post_list = Post.objects.filter(author=request.user).order_by('-pk')
    post_dict = {}
    for post in post_list:
        post_dict[post.pk] = {'likes': get_like_amount(post=post), 'post': post, 'has_liked': has_liked_post(request.user, post), 
        'username': post.author.username, 'comment_count': get_comment_amount(post),
        'comments': get_comments(post)}
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'follower_count': follower_count,
        'following_count': following_count,
        'likes': get_likes(request.user),
        'posts': post_dict,
        'title': f'Your Profile',
    }
    return render(request, 'users/profile.html', context)

