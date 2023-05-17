from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .models import Diary

class Diarylist(ListView):
    model = Diary
    ordering = '-pk'

class DiaryDetail(DetailView):
    model = Diary

class DairyUpdate(UpdateView):
    model = Diary
    fields = ['title', 'content', 'head_image']

    template_name = 'blog/diary_update_form.html'