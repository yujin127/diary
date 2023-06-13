from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'diary'
urlpatterns = [
    path('', views.diary_cal),
    path('diary_detail/<int:pk>/', views.DiaryDetail.as_view(), name='diary_detail'),
    path('diary_form/', views.diary_form, name='diary_form'),
    path('diary_list/',  views.DiaryList.as_view(), name='diary_list'),
    path('diary_update/<int:diary_id>/', views.diary_update, name='diary_update'),
    path('diary_delete/<int:pk>/', views.DiaryDelete.as_view(), name='diary_delete'),
    path('confirmation/', views.confirmation, name='confirmation')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)