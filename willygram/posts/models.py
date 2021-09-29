from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile, UserFollowing
from PIL import Image


class Post(models.Model):
    description = models.TextField(max_length=1000, blank=True, default='')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='posts', null=True)


    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)

            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except: # in event of no image
            pass

class PostLikes(models.Model):
    post_id = models.ForeignKey(Post, related_name="post", on_delete=models.CASCADE)

    liked_by = models.ForeignKey(User, related_name="liked_by", on_delete=models.CASCADE)

    # You can even add info about when user started following
    liked_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class PostComment(models.Model):
    post_id = models.ForeignKey(Post, related_name="post_comment", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="comment_author", on_delete=models.CASCADE)
    content = models.TextField(max_length=400, default='')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

