from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('gastos/', views.gastos, name="gastos"),
    path('ingresos/', views.ingresos, name="ingresos"),
    path('reporte/', views.reporte, name="reporte"),
]
