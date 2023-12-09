from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registo_encomenda/', views.registo_encomenda, name='registo_encomenda'),
]