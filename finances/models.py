from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    """
    Custom user model
    """
    total_amount = models.DecimalField(
        max_digits=100, decimal_places=2, default=0)


class Category(models.Model):
    """
    Category of financial movements model
    """
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " by: " + self.user.username


class Transaction(models.Model):
    """
    Transaction model
    """
    TRANSACTION_TYPES = [
        ("EX", "Expense"),
        ("IN", "Income")
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    transaction_type = models.CharField(
        max_length=15, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=100, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " | " + self.transaction_type
