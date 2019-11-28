from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordChangeForm, ReadOnlyPasswordHashField
# 현재 활성화(active)된 user model 을 return 한다.
from django.contrib.auth import get_user_model
from django import forms
from .models import Guild
# from ckeditor_uploader.widgets import CKEditorUploadingWidget


class GuildForm(forms.ModelForm):

    class Meta:
        model = Guild
        fields = ['name', ]


class CustomPasswordChangeForm(PasswordChangeForm):
    pass


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label='Password',
        help_text='<a href=\"password/\" style="font-weight:bold; text-decoration:underline; color:green">여기서 변경</a>.'
    )

    class Meta:
        model = get_user_model()  # accounts.User
        fields = ['nickname', ]


# 커스터마이징한 유저모데을 인식하지 못해서 직접 get_user_model 함수로
# 유저 모델 정보를 넣어줌
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '본명을 적어주세요',
            }
        ),
    )
    nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '사용할 닉네임을 적어주세요',
            }
        ),
    )
    age = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '나이를 적어주세요',
            }
        ),
        help_text='**만 18세 이상 성인만 가입 가능합니다',
    )
    error_messages = {
        'password_mismatch': '비밀번호를 다시 확인해주세요!',
    }
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text='**영문 대소문자, 숫자 조합 8자리 이상',
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        # help_text='',
    )

    class Meta:
        model = get_user_model()
        # fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
        # fields = ['username', 'nickname', 'age', 'password1', 'password2', ]
        fields = ['username', 'nickname', 'age', ]
        # help_texts = {
            # 'username': 'test',
            # 'age': '안녕',
            # 'password1': '입력',
            # 'password2': '확인'
        # }
