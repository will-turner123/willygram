from django import template
from notif.models import Notification

register = template.Library()

# @register.simple_tag
def notifications_3(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-received_date')[3:].values()
    if notifications.exists():
        notif_count = Notification.objects.filter(recipient=request.user, read=False).count()
    else:
        notif_count = 0
    data = {'valid': True, 'notifications': list(notifications), 'unread_count': notif_count}
    return data

def notification_count(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-received_date')[3:].values()
    if notifications.exists():
        notif_count = Notification.objects.filter(recipient=request.user, read=False).count()
    return notif_count

def my_custom_tag(request):
    return "Hello, world!"