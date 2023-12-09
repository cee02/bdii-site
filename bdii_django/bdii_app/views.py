from django.shortcuts import render
from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def registo_encomenda(request):
    return render(request, 'registo_encomenda.html')