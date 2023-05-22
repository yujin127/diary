from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'diary'
urlpatterns = [
    path('', views.diary_cal),
    path('<int:pk>/', views.DiaryDetail.as_view()),
    path('write_diary/', views.write_diary, name='write_diary'),
    path('diary_save/', views.diary_save, name='diary_save'),
    path('write_diary2/', views.write_diary2, name='write_diary2'),
    path('diary_form/', views.diary_form, name='diary_form'),
    path('diary_list/',  views.DiaryList.as_view(), name='diary_list')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)