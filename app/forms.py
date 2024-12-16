from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .form_validators import validate_email
from django.contrib.auth.forms import AuthenticationForm


class UserCreateForm(forms.ModelForm):
    username = forms.CharField(
    error_messages={
        'required': '',
        'max_length': '',
        'invalid': 'Username ou senha inválidos, digite novamente'
    }
)
    email = forms.EmailField(
        required=True,
        validators=[validate_email])

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
        validators=[validate_password],
    )

    confirm_password = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if not password or not confirm_password:
            raise ValidationError('Por favor, preencha todos os campos obrigatórios.')

        if password != confirm_password:
            raise ValidationError('As senhas não coincidem')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))