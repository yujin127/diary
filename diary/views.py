from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Diary
from .forms import DiaryForm, WriteDiary
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import ListView
from analysis.stat_model.charts import create_bar_chart, create_pie_chart, create_radar_chart
import os
import datetime
from analysis.stat_model.wordcloud_chart import keyword_list, make_wordcloud
from .contents.movie_recommend import movie_recommend
from .contents.music_recommend import music_recommend

@method_decorator(login_required(login_url='common:login'), name='dispatch')
class DiaryList(ListView):
    model = Diary
    ordering = '-pk'

    def get_queryset(self):
        # Get the queryset of diaries for the logged-in user
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset

def diary_cal(request):
    return render(
        request,
        'diary/diary_list2.html'
    )

@method_decorator(login_required(login_url='common:login'), name='dispatch')
class DiaryDetail(DetailView):
    model = Diary
    template_name = 'diary/diary_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diary = self.get_object()
        date = diary.created_at

        radar_image_name = create_radar_chart(diary.author.id, date)
        radar_image_path = os.path.join('analysis/static/image', radar_image_name)
        context['radar_image_name'] = radar_image_name
        context['radar_image_path'] = radar_image_path

        pie_image_name = create_pie_chart(diary.author.id, date)
        pie_image_path = os.path.join('analysis/static/image', pie_image_name)
        context['pie_image_name'] = pie_image_name
        context['pie_image_path'] = pie_image_path

        bar_image_name = create_bar_chart(diary.author.id, date)
        bar_image_path = os.path.join('analysis/static/image', bar_image_name)
        context['bar_image_name'] = bar_image_name
        context['bar_image_path'] = bar_image_path

        keyword = keyword_list(diary.author.id, date, 3)
        context['keyword'] = keyword

        wordcloud_image_name = make_wordcloud(diary.author.id, date)
        wordcloud_image_path = os.path.join('analysis/static/image', wordcloud_image_name)
        context['wordcloud_image_name'] = wordcloud_image_name
        context['wordcloud_image_path'] = wordcloud_image_path

        movie_name, movie_image_name, movie_info = movie_recommend(diary.author.id, date)
        movie_image_name = f'{movie_image_name}.jpg'
        movie_image_path = os.path.join('analysis/static/image', movie_image_name)
        context['movie_name'] = movie_name
        context['movie_image_name'] = movie_image_name
        context['movie_image_path'] = movie_image_path
        context['movie_info'] = movie_info

        music_image_name, music_title, music_artist = music_recommend(diary.author.id, date)
        music_image_path = os.path.join('analysis/static/image', music_image_name)
        context['music_title'] = music_title
        context['music_artist'] = music_artist
        context['music_image_name'] = music_image_name
        context['music_image_path'] = music_image_path

        return context
@login_required(login_url='common:login')
def diary_form(request):
    today = timezone.now().date()
    existing_diary = Diary.objects.filter(author=request.user, created_at=today).first()

    if existing_diary:
        messages.info(request, '하루에 하나의 일기만 작성할 수 있습니다.')
        return redirect('diary:diary_detail', pk=existing_diary.pk)

    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.author = request.user
            diary.save()
            return redirect('/diary/diary_detail/')
    else:
        form = DiaryForm()

    return render(request, 'diary/diary_form.html', {'form': form})

def diary_update(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    if request.user != diary.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('diary:diary_detail', diary_id=diary.id)
    if request.method == "POST":
        form = DiaryForm(request.POST, instance=diary)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.updated_at = timezone.now()
            diary.save()
            return redirect('diary:diary_detail', pk=diary.id)
    else:
        form = DiaryForm(instance=diary)
    return render(request, 'diary/diary_form.html', {'form':form})

class DiaryDelete(DeleteView):
    model = Diary
    template_name = 'diary/diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')