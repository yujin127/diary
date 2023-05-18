from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.Diarylist.as_view(), name='diary_list'),
    path('<int:pk>/', views.DiaryDetail.as_view()),
    path('write_diary/', views.write_diary),
    path('diary_cal/', views.diary_cal)
]