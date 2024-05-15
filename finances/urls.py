from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('expenses/', views.expenses, name="expenses"),
    path('incomes/', views.incomes, name="incomes"),
    path('report/', views.report, name="report"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register")
]
