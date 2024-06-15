from django import forms
from django.contrib.auth.forms import UserCreationForm
from core_cadastros.models import CustomUser, Enterprise

class EnterpriseForm(forms.ModelForm):
    class Meta:
        model = Enterprise
        fields = ['tipo', 'nome', 'id_nacional', 'telefone', 'email', 'address', 'cnpj']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class CadastroForm(forms.Form):
    tipo = forms.CharField(widget=forms.HiddenInput())
    nome = forms.CharField(max_length=100, required=True)
    id_nacional = forms.CharField(max_length=18, required=True)  # CPF ou CNPJ
    telefone = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    senha1 = forms.CharField(widget=forms.PasswordInput(), required=True)
    senha2 = forms.CharField(widget=forms.PasswordInput(), required=True)
