from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import datetime

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    # calculate sign here?
    # following = models.ManyToManyField('User', blank=True, related_name='followers', symmetrical=False)
    # followers = models.ManyToManyField('User', blank=True, related_name='following')
    # verified = False
    bio = models.CharField(max_length=300, blank=True, default='')

    # follows = models.ManyToManyField('self', related_name='follows', symmetrical=False)
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)

    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)