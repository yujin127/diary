from django import forms
from single_pages.models import UserInfo


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['birth', 'school', 'number', 'address', 'mbti', 'hobby']
        labels = {
            'birth':'생일',
            'school':'학교',
            'number': '번호',
            'address': '주소',
            'mbti': 'mbti',
            'hobby': '취미',
        }