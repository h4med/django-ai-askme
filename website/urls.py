from django.urls import path
from . import views
from . import viewsf

urlpatterns = [
    path('', views.home, name='home'),
    path('write-code/', views.write_code, name='write_code'),
    path('ask-me/', views.ask_me, name='ask_me'),
    path('ask-me-fa/', viewsf.AskMeView.as_view(), name='ask_me_fa'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('register/',views.register_user, name='register'),
    path('ask-me-archive/',views.ask_me_arch, name='ask_me_arch'),
    path('edit-me/',views.edit_me, name='edit_me'),
]
