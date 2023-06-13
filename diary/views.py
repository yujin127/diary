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
from analysis.stat_model.charts import create_bar_chart, create_pie_chart, create_radar_chart, \
    create_bar_chart_per, create_bar_plot
import os
import datetime
from analysis.stat_model.wordcloud_chart import keyword_list, make_wordcloud
from .contents.movie_recommend import movie_recommend
from .contents.music_recommend import music_recommend
from .contents.book_recommend import book_recommend
from analysis.stat_model.predict_func import count_emotion, predict
import torch
from transformers import BertModel
import gluonnlp as nlp

from kobert_tokenizer import KoBERTTokenizer
from analysis.stat_model.MyBert import BERTDataset, BERTClassifier
from diary.models import Diary

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

        # 이미지 파일 경로 설정
        radar_image_name, a = create_radar_chart(diary.author.id, date)
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

        per_bar_image_name = create_bar_chart_per(diary.author.id, date)
        per_bar_image_path = os.path.join('analysis/static/image', per_bar_image_name)
        context['per_bar_image_name'] = per_bar_image_name
        context['per_bar_image_path'] = per_bar_image_path

        barplot_image_name = create_bar_plot(diary.author.id, date)
        barplot_image_path = os.path.join('analysis/static/image', barplot_image_name)
        context['barplot_image_name'] = barplot_image_name
        context['barplot_image_path'] = barplot_image_path

        keyword = keyword_list(diary.author.id, date, 6)
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

        music_image_name, music_title, music_artist, album_link = music_recommend(diary.author.id, date)
        music_image_path = os.path.join('analysis/static/image', music_image_name)
        context['music_title'] = music_title
        context['music_artist'] = music_artist
        context['music_image_name'] = music_image_name
        context['music_image_path'] = music_image_path
        context['album_link'] = album_link

        book_title, book_author, book_image_name, emotion, book_info = book_recommend(diary.author.id, date)
        book_image_name = f'{book_image_name}.jpg'
        book_image_path = os.path.join('analysis/static/image', book_image_name)
        context['book_title'] = book_title
        context['book_author'] = book_author
        context['book_image_name'] = book_image_name
        context['book_image_path'] = book_image_path
        context['emotion'] = emotion
        context['book_info'] = book_info

        emotion_images = {
            '슬픔': '슬픔.jpg',
            '공포': '공포.jpg',
            '놀람': '놀람.jpg',
            '분노': '분노.jpg',
            '기쁨': '기쁨.jpg',
            '행복': '행복.jpg',
        }

        emotion_data = diary.emotion_data

        starting_rank = 1
        ranking = [(starting_rank + i, item) for i, item in enumerate(keyword)]
        context['ranking'] = ranking

        if emotion_data is None:
            context['emotion_counts'] = None
            context['emotion'] = None
        else:
            emotion_counts = count_emotion(emotion_data)
            context['emotion_counts'] = emotion_counts
            context['emotion'] = max(emotion_counts, key=emotion_counts.get)

        context['emotion_images'] = emotion_images

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

            PATH = 'analysis/stat_model/'

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
            vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')

            # BertClassifier 오류 발생 해결 방안
            # bertmodel = BertModel.from_pretrained("bert-base-multilingual-cased")
            bertmodel = BertModel.from_pretrained("skt/kobert-base-v1")
            model = BERTClassifier(bert=bertmodel, dr_rate=0.5).to(device)

            # model = torch.load(PATH + 'BestModel.pt', map_location=device)
            model.load_state_dict(torch.load(PATH + 'model_state_dict_final.pt', map_location=device))
            model.to(device)
            model.eval()

            sentences = form.cleaned_data['content']

            d_l = sentences.split('.')
            total_emotion = []
            for i in range(len(d_l) - 1):
                # total_emotion.append(predict(d_l[i], model, tokenizer, vocab))
                emotions = predict(d_l[i], model, tokenizer, vocab)
                total_emotion.extend(emotions)

            if '불안' in total_emotion:
                index1 = total_emotion.index('불안')
                total_emotion[index1] = '슬픔'
            elif '당황' in total_emotion:
                index2 = total_emotion.index('당황')
                total_emotion[index2] = '슬픔'
            elif '상처' in total_emotion:
                index3 = total_emotion.index('상처')
                total_emotion[index3] = '슬픔'
            elif '혐오' in total_emotion:
                index4 = total_emotion.index('혐오')
                total_emotion[index4] = '분노'
            else:
                total_emotion = total_emotion
            diary.emotion_data = total_emotion

            diary.save()
            return redirect('diary:confirmation')
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

def confirmation(request):
    today = timezone.now().date()
    existing_diary = Diary.objects.filter(author=request.user, created_at=today).first()

    if existing_diary:
        pk = existing_diary.pk
        return render(request, 'diary/confirmation.html', {'pk': pk})