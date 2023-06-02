from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label='email')
    name = forms.CharField(max_length=16, label='name')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name']  # Save the name value to the first_name field
        if commit:
            user.save()
        return user