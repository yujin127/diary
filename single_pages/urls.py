from django.urls import path
from . import views

app_name = 'single_pages'
urlpatterns = [
    path('about_me/', views.about_me),
    path('', views.landing, name='landing'),
    path('today_result/', views.today_result),
    path('stacked_result/', views.stacked_result),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup')
]