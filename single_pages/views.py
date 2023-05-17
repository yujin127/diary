from django.shortcuts import render
from diary.models import Diary

def landing(request):
    recent_diary = Diary.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_diary': recent_diary,
        }
    )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )

def today_result(request):
    return render(
        request,
        'single_pages/today_result.html'
    )

def stacked_result(request):
    return render(
        request,
        'single_pages/stacked_result.html'
    )