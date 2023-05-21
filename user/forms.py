from django import forms
from .models import User
from argon2 import PasswordHasher, exceptions

class SignupForm(forms.ModelForm):
    user_id = forms.CharField(
        label='ID',
        required=True,
        widget=forms.TextInput(
            attrs={'class':'user-id'}
        ), error_messages={'required':'아이디를 입력해주세요',
                           'unique':'이미 사용되고 있는 아이디입니다'}
    )
    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'user-pw'}
        ), error_messages={'required': '비밀번호를 입력해주세요'}
    )
    password_ck = forms.CharField(
        label='Password_ck',
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'user-pw-ck'}
        ), error_messages={'required': '비밀번호가 일치하지 않습니다'}
    )
    name = forms.CharField(
        label='name',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'user-name'}
        ), error_messages={'required': '이름을 입력해주세요'}
    )
    email = forms.CharField(
        label='email',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'user-email'}
        ), error_messages={'required': '이메일을 입력해주세요'}
    )

    field_order = [
        'user_id',
        'password',
        'password_ck',
        'email',
        'name'
    ]
    class Meta:
        model = User
        fields = [
            'user_id',
            'password',
            'email',
            'name'
        ]

    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get('user_id', '')
        password = cleaned_data.get('password', '')
        password_ck = cleaned_data.get('password_ck', '')
        email = cleaned_data.get('email', '')
        name = cleaned_data.get('name', '')

        if password != password_ck:
            return self.add_error('password_ck', '비밀번호가 다릅니다')
        elif not (4 <= len(user_id) <= 16):
            return self.add_error('user_id', '아이디는 4~16자로 입력해주세요')
        elif 8 > len(password):
            return self.add_error('password', '비밀번호는 8자 이상으로 입력해주세요')
        else:
            self.user_id = user_id
            self.password = PasswordHasher().hash(password)
            self.password_ck = password_ck
            self.email = email
            self.name = name

class LoginForm(forms.Form):
    user_id = forms.CharField(
        max_length=32, label='ID', required=True,
        widget=forms.TextInput(attrs={'class':'user-id'}),
        error_messages={'required':'아이디를 입력해주세요'}
    )
    password = forms.CharField(
        max_length=128, label='Password', required=True,
        widget=forms.PasswordInput(attrs={'class': 'user-pw'}),
        error_messages={'required': '비밀번호를 입력해주세요'}
    )
    field_order = ['user_id', 'password']

    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get('user_id', '')
        password = cleaned_data.get('password', '')

        if user_id == '':
            return self.add_error('user_id'), '아이디를 다시 입력해주세요'
        elif password == '':
            return self.add_error('password'), '비밀번호를 다시 입력해주세요'
        else:
            try:
                user = User.objects.get(user_id = user_id)
            except User.DoesNotExist:
                return self.add_error('user_id', '아이디가 존재하지 않습니다')

            try:
                PasswordHasher().verify(user.password, password)
            except exceptions.VerifyMismatchError:
                return self.add_error('password', '비밀번호가 다릅니다')

            self.login_session = user.user_id