from django import forms
from diary.models import Diary

class WriteDiary(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'content','author']
        labels = {
            'title':'제목',
            'content':'일기',
            'author':'작성자'
        }

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'content', 'head_image']
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control mt-2",
                }
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control mt-2", "rows": 10}
            ),

        }
        labels = {
            'title':'제목',
            'content':'일기',
            'head_image':'이미지'
        }