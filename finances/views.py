from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def inicio(request):
    """
    El inicio del sistema
    """
    return render(request, 'inicio.html')


def gastos(request):
    """
    Vista de gastos del sistema. 
    Enlista todos los gastos hechos por el usuario.
    """
    return render(request, 'gastos.html')


def ingresos(request):
    """
    Vista de ingresos del sistema. 
    Enlista todos los ingresos que ha tenido el usuario.
    """
    return render(request, 'ingresos.html')


def reporte(request):
    """
    Vista de reporte de ingresos y gastos.
    """
    return render(request, 'reporte.html')
