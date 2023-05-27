from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'diary'
urlpatterns = [
    path('', views.diary_cal),
    path('diary_detail/<int:pk>/', views.DiaryDetail.as_view(), name='diary_detail'),
    path('write_diary/', views.write_diary, name='write_diary'),
    path('diary_save/', views.diary_save, name='diary_save'),
    path('diary_form/', views.diary_form, name='diary_form'),
    path('diary_list/',  views.DiaryList.as_view(), name='diary_list'),
    path('diary_update/<int:diary_id>/', views.diary_update, name='diary_update'),
    path('diary_delete/<int:pk>/',  views.DiaryDelete.as_view(), name='diary_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)