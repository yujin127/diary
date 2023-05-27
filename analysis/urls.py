from django.urls import path
from . import views


app_name = 'analysis'
urlpatterns = [
    path('today_result/', views.today_result, name='today_result'),
    path('stacked_result/', views.stacked_result, name='stacked_result'),
    ]
