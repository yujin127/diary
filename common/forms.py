from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label='email')
    name = forms.CharField(max_length=16, label='name')

    birthday = forms.DateField(label='birthday')
    school = forms.CharField(max_length=32, label='school')
    phone_number = forms.IntegerField(label='phone_number')
    address = forms.CharField(label='address')
    mbti = forms.CharField(max_length=4, min_length=4, label='mbti')
    hobby = forms.CharField(label='hobby')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'name', 'birthday',
                  'school', 'phone_number', 'address', 'mbti', 'hobby')