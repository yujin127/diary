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

@method_decorator(login_required(login_url='common:login'), name='dispatch')
class DiaryList(ListView):
    model = Diary
    ordering = '-pk'


def diary_cal(request):
    return render(
        request,
        'diary/diary_list2.html'
    )

@method_decorator(login_required(login_url='common:login'), name='dispatch')
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
        diary.author = request.user

        diary.save()
    return redirect('/home/')

# @login_required(login_url='common:login')
# def diary_form(request):
#     if request.method == 'POST' or request.method == 'FILES':
#         form = DiaryForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             form.author = request.user
#             return redirect('/home/')
#     else:
#         form = DiaryForm()
#     return render(request, 'diary/diary_form.html', {'form':form})


@login_required(login_url='common:login')
def diary_form(request):
    if request.method == 'POST' or request.method == 'FILES':
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.author = request.user
            diary.save()
            return redirect('/home/')
    else:
        form = DiaryForm()
    return render(request, 'diary/diary_form.html', {'form':form})

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

# def diary_delete(request, diary_id):
#     diary = get_object_or_404(Diary, pk=diary_id)
#     if request.user != diary.author:
#         messages.error(request, '삭제권한이 없습니다')
#         return redirect('diary:diary_detail', diary_id=diary.id)
#     if request.method == "POST":
#         diary.delete()
#         return redirect('diary:diary_list')
#     return render(request, 'diary/diary_delete.html', {'diary': diary})

class DiaryDelete(DeleteView):
    model = Diary
    template_name = 'diary/diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')