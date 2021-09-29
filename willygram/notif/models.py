from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_notification', default='')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient_notification', default='')
    message = models.TextField()
    read = models.BooleanField(default=False)
    received_date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)