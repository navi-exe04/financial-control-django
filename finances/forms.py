from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, CustomUser, Transaction

class CustomUserForm(UserCreationForm):
    """
    Define the custom user form
    """
    class Meta:
        """
        Properties
        """
        model = CustomUser
        fields = ['username', 'password1', 'password2']

class CategoryForm(forms.ModelForm):
    """
    Define the category form
    """
    class Meta:
        """
        Properties
        """
        model = Category
        fields = ['title', 'description']


class TransactionForm(forms.ModelForm):
    """
    Define the transaction form
    """
    class Meta:
        """
        Properties
        """
        model = Transaction
        fields = [
            'title', 
            'description', 
            'transaction_type', 
            'amount',
            'category'
        ]
