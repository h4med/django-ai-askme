from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('write-code/', views.write_code, name='write_code'),
    path('ask-me/', views.ask_me, name='ask_me'),
]
