from django import forms
from .models import Post, PostLikes

# class DateInput():
#     birthday = forms.DateInput(widgets=DateInput)
#     fields = ['birthday']



class PostCreateForm(forms.ModelForm):
    description = forms.CharField(required=True, max_length=1000, widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'contentInput', 'required': '', 'placeholder': 'Enter your required post text here, with an optional image', 'name': 'description'}))
    image = forms.FileField(required=False)
    class Meta:
        model = Post
        fields = ['description', 'image']

