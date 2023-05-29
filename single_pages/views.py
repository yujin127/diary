from django.shortcuts import render
from diary.models import Diary
from django.contrib.auth.decorators import login_required

def landing(request):
    recent_diary = Diary.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_diary': recent_diary,
        }
    )

# @login_required(login_url='common:login')
# def about_me(request):
#     return render(
#         request,
#         'single_pages/about_me.html', {'request':request}
#     )

@login_required(login_url='common:login')
def about_me(request):
    user = request.user
    return render(request, 'single_pages/about_me.html', {'user': user})