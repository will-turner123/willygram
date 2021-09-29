from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Create your views here.
from .models import Notification
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import humanize
from datetime import datetime
from django.utils import timezone


def list_notifications(request):
    notif = Notification.objects.filter(recipient=request.user).order_by('-received_date') 
    print(notif)
    return render(request, 'notif/list.html', {'notifications': notif})


def get_notifications(request):
    if request.is_ajax and request.method == "GET":
        amount = request.GET.get("amount")
        notifications = Notification.objects.filter(recipient=request.user).order_by('received_date').values()[:50]
        if notifications.exists():
            notif_count = Notification.objects.filter(recipient=request.user, read=False).count()
        else:
            notif_count = 0
        for notif in notifications:
            notif['sender_id'] = User.objects.get(pk=notif['sender_id']).username
            notif['recipient_id'] =  User.objects.get(pk=notif['recipient_id']).username
            notif['sender_url'] = reverse('view-profile', kwargs={'username': notif['sender_id']})
            print(notif['received_date'])

            notif['pretty_date'] = humanize.naturaltime(notif['received_date'], when=timezone.now())
        data = {'valid': True, 'notifications': list(notifications), 'unread_count': notif_count}
        return JsonResponse(data, status=200)
    return JsonResponse({}, status=400)

def mark_as_read(request):
    if request.is_ajax and request.method == "GET":
        notifications = Notification.objects.filter(recipient=request.user, read=False)
        if notifications.exists():
            notifications.update(read=True)
            return JsonResponse({'valid': True}, status=200)
    return JsonResponse({}, status=400)