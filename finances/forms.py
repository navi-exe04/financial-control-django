from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, CustomUser

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description']
