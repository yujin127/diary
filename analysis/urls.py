from django.urls import path
from . import views


app_name = 'analysis'
urlpatterns = [
    path('stacked_result/', views.stacked_result, name='stacked_result'),
    ]
