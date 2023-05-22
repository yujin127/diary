from django import forms
from diary.models import Diary

class WriteDiary(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'content']
        labels = {
            'title':'제목',
            'content':'일기'
        }


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'content', 'head_image']