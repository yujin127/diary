from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.Postlist.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetail.as_view()),
]