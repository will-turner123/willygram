from django.db.models.signals import post_save, post_init, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, UserFollowing


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(f'Created!!')
        Profile.objects.create(user=instance)
        UserFollowing.objects.create(user_id=instance, following_user_id=instance) # follows self