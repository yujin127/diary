from django.shortcuts import render
from diary.models import Diary
from django.contrib.auth.decorators import login_required
from .forms import UserInfoForm
from .models import UserInfo
from django.shortcuts import redirect

def landing(request):
    recent_diary = Diary.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_diary': recent_diary,
        }
    )


@login_required(login_url='common:login')
def about_me(request):
        info = UserInfo.objects.filter(username=request.user)
        return render(request,'single_pages/about_me.html', {'info':info})

@login_required(login_url='common:login')
def info_view(request):
        if request.method == 'POST':
            form = UserInfoForm(request.POST, request.FILES)
            if form.is_valid():
                newinfo = form.save(commit=False)
                newinfo.username = request.user
                newinfo.id=1
                newinfo.save()
                return redirect('/about_me/')
        else:
            form = UserInfoForm()
        return render(request, 'single_pages/info.html', {'form': form})