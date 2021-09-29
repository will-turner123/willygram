from django.db.models.signals import post_save, post_init, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Notification
from posts.models import Profile, UserFollowing, PostLikes, PostComment, Post
from dm.models import Channel, ChannelMessage

# sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sender_notification')
# recipient = models.ManyToManyField(User)
# message = models.TextField()
# read = models.BooleanField(default=False)
# recieved_date = models.DateTimeField(auto_now_add=True)
def create_notification(author, recipient, message):
    Notification.objects.create(sender=author, recipient=recipient, message=message, read=False)


# post_id = models.ForeignKey(Post, related_name="post", on_delete=models.CASCADE)

# liked_by = models.ForeignKey(User, related_name="liked_by", on_delete=models.CASCADE)

# # You can even add info about when user started following
# liked_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=PostLikes)
def send_like_notif(sender, instance, created, **kwargs):
    print(f'here')
    if created:
        item = Notification()
        item.sender = instance.liked_by
        item.recipient = instance.post_id.author
        item.message = "liked your post"
        item.save()
        # create_notification(sender=instance.liked_by, recipient=send_id, message="liked your post")


@receiver(post_save, sender=PostComment)
def send_comment_notif(sender, instance, created, **kwargs):
    if created:
        item = Notification()
        item.sender = instance.author
        item.recipient = instance.post_id.author
        item.message = "commented on your post"
        item.save()


    # user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    # following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    # created = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=UserFollowing)
def send_follow_notif(sender, instance, created, **kwargs):
    if created:
        item = Notification()
        item.sender = instance.following_user_id
        item.recipient = instance.user_id
        item.message = "followed you"
        if item.sender != item.recipient:
            item.save()


# TODO: signal to create message on ChannelMessage if ChannelMessage.channel.users != request.user and user in channel
@receiver(post_save, sender=ChannelMessage)
def send_message_notif(sender, instance, created, **kwargs):
    if created:
        item = Notification()
        item.sender = instance.user
        query = Channel.objects.filter(id=instance.channel.id).first()
        print(query.users)
        for user in query.users.all():
            if user != instance.user:
                recip = user
        item.recipient = recip
        item.message = "sent you a message"
        if item.sender != item.recipient:
            item.save()

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         print(f'Created!!')
#         Profile.objects.create(user=instance)
#         UserFollowing.objects.create(user=instance, following_user_id=instance) # follows self