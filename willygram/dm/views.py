from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User

from django.shortcuts import render
from users.models import Profile
from .forms import ChannelMessageForm
from .models import Channel, ChannelMessage
from notif.models import Notification


class ChannelFormMixin(FormMixin):
    form_class = ChannelMessageForm
    # success_url = './'
    def get_success_url(self):
        return self.request.path
    # handle the form with this mixin
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        form = self.get_form()
        if form.is_valid():
            channel = self.get_object()
            user = self.request.user
            content = form.cleaned_data.get("content")
            channel_obj = ChannelMessage.objects.create(channel=channel, user=user, content=content)
            if request.is_ajax():
                # Django Rest Framework
                return JsonResponse({"content": channel_obj.content, "username": channel_obj.user.username }, status=201)
            return super().form_valid(form)
        else:
            if request.is_ajax():
                return JsonResponse({"errors": form.errors}, status=400)
            return super().form_invalid(form)



class ChannelDetailView(LoginRequiredMixin, ChannelFormMixin, DetailView):
    template_name = 'dm/private_message.html'
    queryset = Channel.objects.all() 
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = context['object']
        # if self.request.user not in obj.users.all():
        #     raise PermissionDenied
        context['is_channel_member'] = self.request.user in obj.users.all()
        return context
    
    # def get_queryset(self):
    #     user = self.request.user # definitely a user
    #     username = user.username
    #     qs = Channel.objects.all().filter_by_username(username)
    #     return qs

class PrivateMessageDetailView(LoginRequiredMixin, ChannelFormMixin, DetailView):
    template_name = 'dm/private_message.html'
    def get_object(self, *args, **kwargs):
        print('here2')
        username = self.kwargs.get("username")
        my_username = self.request.user.username
        if username == my_username:
            my_channel_obj, _ = Channel.objects.get_or_create_current_user_private_message(self.request.user)
            return my_channel_obj
        channel_obj, _ = Channel.objects.get_or_create_private_message(my_username, username)
        if channel_obj == None:
            raise Http404
        channel_query = Channel.objects.get_queryset().filter_by_username(my_username).all()
        print('*' * 10)
        # get all rooms a user is in
        has_dms_with = []
        data = []
        for query in channel_query:
            for user in query.channeluser_set.all():
                if user.user != my_username:
                    data.append(query)
    
            # print(thing.users)
            # print(f'{my_username} is in a chatroom with {query.filter()}')
        # print(f'query:')
        # for query in my_cool_query:
        #     print(query)
        return channel_obj

def get_object(request, *args, **kwargs):
    print('here2')
    username = kwargs.get("username")
    my_username = request.user.username
    if username == my_username:
        my_channel_obj, _ = Channel.objects.get_or_create_current_user_private_message(kwargs.request.user)
        return my_channel_obj
    channel_obj, _ = Channel.objects.get_or_create_private_message(my_username, username)
    if channel_obj == None:
        raise Http404
    channel_query = Channel.objects.get_queryset().filter_by_username(my_username).all()
    print('*' * 10)
    # get all rooms a user is in
    has_dms_with = []
    data = []
    for query in channel_query:
        for user in query.channeluser_set.all():
            if user.user != my_username:
                data.append(query)

        # print(thing.users)
        # print(f'{my_username} is in a chatroom with {query.filter()}')
    # print(f'query:')
    # for query in my_cool_query:
    #     print(query)
    return channel_obj



def private_message(request, username=None):
    if request.user.is_authenticated:
        if request.POST:
            if not request.user.is_authenticated:
                raise PermissionDenied
            form = ChannelMessageForm(request.POST)
            if form.is_valid():
                channel = get_object(request, username=username)
                user = request.user
                content = form.cleaned_data.get("content")
                channel_obj = ChannelMessage.objects.create(channel=channel, user=user, content=content)
                if request.is_ajax():
                    # Django Rest Framework
                    return JsonResponse({"content": channel_obj.content, "username": channel_obj.user.username }, status=201)
                return super().form_valid(form)
            else:
                if request.is_ajax():
                    return JsonResponse({"errors": form.errors}, status=400)
                return super().form_invalid(form)
        form = ChannelMessageForm()

        send_user = User.objects.get(username=username)
        ex = Notification.objects.filter(recipient=request.user, sender=send_user, message='sent you a message', read=False)
        if ex.exists():
            ex.update(read=True)
        if request.user.username == username:
            channel_obj, _ = Channel.objects.get_or_create_current_user_private_message(request.user)
        else:
            channel_obj, _ = Channel.objects.get_or_create_private_message(request.user.username, username)
        if channel_obj == None:
            raise Http404
        channel_query = Channel.objects.get_queryset().filter_by_username(request.user)
        data = []
        for query in channel_query:
            for user in query.channeluser_set.all():
                if user.user != request.user:
                    data.append(query)
        data = list(sorted(data, key=lambda k: k.pk, reverse=True))
        data_dict = {}
        for item in data:
            # obj = Channel.objects.get_queryset().filter_by_username(request.user).
            for user in item.channeluser_set.all():
                if user.user != request.user:
                    user_with = user.user
            has_read_message = Notification.objects.filter(recipient=request.user, sender=user_with, message='sent you a message', read=False).count()
            print(has_read_message)
            if has_read_message > 0:
                has_read_message = True
            else:
                has_read_message= False
            data_dict[item.pk] = {
                'channel_obj': Channel.objects.get_queryset().filter_by_username(request.user),
                'user_with': user_with,
                'read_message': has_read_message,
            }
        return render(request, 'dm/private_message.html', {'username': username, 'object': channel_obj, 'data': data_dict, 'form': form, 'title': f'Your messages'})
    raise Http404

def get_private_messages(request):
    if request.user.is_authenticated:
        channel_query = Channel.objects.get_queryset().filter_by_username(request.user)
        data = []
        for query in channel_query:
            for user in query.channeluser_set.all():
                if user.user != request.user:
                    data.append(query)
        data = list(sorted(data, key=lambda k: k.pk, reverse=True))
        data_dict = {}
        for item in data:
            # obj = Channel.objects.get_queryset().filter_by_username(request.user).
            for user in item.channeluser_set.all():
                if user.user != request.user:
                    user_with = user.user
            has_read_message = Notification.objects.filter(recipient=request.user, sender=user_with, message='sent you a message', read=False).count()
            print(has_read_message)
            if has_read_message > 0:
                has_read_message = True
            else:
                has_read_message= False
            data_dict[item.pk] = {
                'channel_obj': Channel.objects.get_queryset().filter_by_username(request.user),
                'user_with': user_with,
                'read_message': has_read_message,
            }


# Create your views here.
def private_message_view(request, username, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponse("Nope..")
    my_username = request.user.username
    channel_obj, created = Channel.objects.get_or_create_private_message(my_username, username)
    if created:
        print("yes it was")
    channel_users = channel_obj.channeluser_set.all().values("user__username")
    print(channel_users)
    channel_messages = channel_obj.channelmessage_set.all()
    print(channel_messages.values("content"))
    return HttpResponse(f"channel items - {channel_obj.id}")


def mark_as_read(request):
    if request.is_ajax and request.method == "GET":
        sender = request.GET.get("sender")
        notifications = Notification.objects.filter(recipient=request.user, read=False, sender=sender, message='sent you a message')
        if notifications.exists():
            notifications.update(read=True)
            return JsonResponse({'valid': True}, status=200)
    return JsonResponse({}, status=400)