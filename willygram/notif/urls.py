from django.urls import path
from .views import (list_notifications, get_notifications, mark_as_read)

urlpatterns = [
    path('notifications/list/', list_notifications, name='list-notifications'),
    path('notifications/get/', get_notifications, name='get-notifications'),
    path('notifications/read/', mark_as_read, name='read-notifications'),
] 