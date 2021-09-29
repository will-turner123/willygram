from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

# class DateInput():
#     birthday = forms.DateInput(widgets=DateInput)
#     fields = ['birthday']

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', "id": "id_username", "autofocus": "", 
        "placeholder": "Username", "required": "", "autocapitalize": "none", "name": "username", "aria-describedby": "usernameHelp"}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Password',
            'id': 'id_password',
            "required": "", 
            "autocapitalize": "none",
            "autocomplete": "current-password",
            "name": "password",
            "aria-describedby": "passwordHelp",
        }
    ))



class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-user', 'id': 'emailInput', 'required': '', 'placeholder': 'Email'}
    ))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'id': 'usernameInput', 'required': '', 'placeholder': 'Username'}
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-user',
            'id': 'password1Input',
            'required': '',
            'placeholder': 'Password'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-user',
            'id': 'password2Input',
            'required': '',
            'placeholder': 'Password confirmation'
        }
    ))
    # birthday = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'id': 'emailInput', 'required': '', 'placeholder': 'Email'}
    ))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'usernameInput', 'required': '', 'placeholder': 'Username'}
    ))
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user')
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields('username') = current_user


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=300, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'bioInput', 'placeholder': 'Bio'}
    ))
    class Meta:
        model = Profile
        fields = ['bio', 'image']
    
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user')
        bio = current_user.profile.bio
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields('bio') = bio





class UserBirthdayForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Profile
        fields = ['birthday']
