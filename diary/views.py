from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Diary

class Postlist(ListView):
    model = Diary
    ordering = '-pk'

class PostDetail(DetailView):
    model = Diary
