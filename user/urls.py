from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('login1/', views.login1, name='login1'),
    path('signup1/', views.signup1, name='signup1'),
    ]