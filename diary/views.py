from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Diary
from .forms import WriteDiary, DiaryForm
from django.utils import timezone

class DiaryList(ListView):
    model = Diary
    ordering = '-pk'

def diary_cal(request):
    return render(
        request,
        'diary/diary_list2.html'
    )

class DiaryDetail(DetailView):
    model = Diary

def write_diary(request):
    if request.method == 'POST':
        form = WriteDiary(request.POST)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.create_date = timezone.now()
            diary.save()
            return redirect('/home/today_result/')
    else:
        form = WriteDiary()
    context = {'form':form}
    return render(request, 'diary/diary_form_fin.html', context)

def diary_save(request):
    if request.method == 'POST':
        diary = Diary()

        diary.title = request.POST['title']
        diary.content = request.POST['content']
        diary.created_at = timezone.now()

        diary.save()
    return redirect('/home/')

def write_diary2(request):
    return render(request, 'diary/write_diary2.html')

def diary_form(request):
    if request.method == 'POST' or request.method == 'FILES':
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/home/')
    else:
        form = DiaryForm()
    return render(request, 'diary/diary_form.html', {'form':form})
