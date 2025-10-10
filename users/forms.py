from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    avatar = forms.ImageField(required=False, label='Аватар')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'avatar')
        labels = {
            'username': 'Имя пользователя',
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'avatar': 'Аватар',
        }