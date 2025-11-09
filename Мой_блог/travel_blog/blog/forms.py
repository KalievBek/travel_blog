from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Ваше имя'),
                'maxlength': 100
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Ваш комментарий (до 500 символов)'),
                'maxlength': 500
            }),
        }
        labels = {
            'author': _('Имя'),
            'text': _('Комментарий'),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            self.fields['author'].initial = self.user.username
            self.fields['author'].widget.attrs['readonly'] = True

    def clean_author(self):
        if self.user and self.user.is_authenticated:
            return self.user.username
        return self.cleaned_data['author']

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        text = text.strip()
        if not text:
            raise forms.ValidationError(_("Комментарий не может быть пустым."))
        if len(text) > 500:
            raise forms.ValidationError(_("Комментарий не должен превышать 500 символов."))
        return text

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Введите ваш email')})
    )
    username = forms.CharField(
        label=_("Имя пользователя"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Введите имя пользователя')})
    )
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Введите пароль')})
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Повторите пароль')})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Имя пользователя"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Введите имя пользователя')})
    )
    password = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Введите пароль')})
    )