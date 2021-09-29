from django import forms

class ChannelMessageForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={"class": "chat-body answer-add",'placeholder':"Write a message"}), label='')