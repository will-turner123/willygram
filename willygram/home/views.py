from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('feed'))
    else:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'home/index.html')


def search_user(request):
    if request.is_ajax and request.method == "GET":
        search_user = request.GET.get("user")
        search_user = search_user.replace('/u/', '')
        search_user = search_user.replace('u/', '')
        to_search = User.objects.filter(username=search_user)
        if to_search.exists():
            print(f'here')
            to_search = to_search.first()
            return HttpResponseRedirect(reverse('view-profile', args=[search_user]))
    messages.alert(f'Unable to find user')
    return HttpResponseRedirect(reverse('feed'))