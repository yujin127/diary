from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.diary_cal),
    path('<int:pk>/', views.DiaryDetail.as_view()),
    path('write_diary/', views.write_diary),
    path('diary_cal/', views.diary_cal)
]