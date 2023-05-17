from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Diary

class Diarylist(ListView):
    model = Diary
    ordering = '-pk'

class DiaryDetail(DetailView):
    model = Diary

class DiaryCreate(CreateView):
    model = Diary
    fields = ['title', 'content', 'head_image']


# def write_diary(request):
#     return render(
#         request,
#         'diary/write_diary2.html'
#     )
