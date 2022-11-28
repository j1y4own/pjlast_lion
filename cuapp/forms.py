from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm, UserCreationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(forms.UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','password1', 'password2', 'age', 'address', 'brithday', 'user_image' ]

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['user_image']