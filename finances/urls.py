from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('create_transaction/', views.CreateTransactionView.as_view(), name="create_transaction"),
    path('create_category/', views.CreateCategoryView.as_view(), name="create_category"),
    path('expenses/', views.ExpensesView.as_view(), name="expenses"),
    path('incomes/', views.IncomesView.as_view(), name="incomes"),
    path('report/', views.ReportView.as_view(), name="report"),
    path('login/', views.LoginUserView.as_view(), name="login"),
    path('logout/', views.LogoutUserView.as_view(), name="logout"),
    path('register/', views.RegisterUserView.as_view(), name="register")
]
