# C:\Users\gusta\OneDrive\Área de Trabalho\Neuron_Hub\neuron_hub\core_website\views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django_tenants.utils import schema_context
from core_tenants.models import Tenant, Domain
from core_cadastros.models import CustomUser, Enterprise
from .forms import CadastroForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection

def cadastro_novo_negocio(request):
    email_exists = False
    id_nacional_exists = False
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['tipo']
            nome = form.cleaned_data['nome']
            id_nacional = form.cleaned_data['id_nacional']
            telefone = form.cleaned_data['telefone']
            email = form.cleaned_data['email']
            senha1 = form.cleaned_data['senha1']
            senha2 = form.cleaned_data['senha2']

            if senha1 != senha2:
                messages.error(request, "As senhas não coincidem.")
                return render(request, 'core_website/cadastrar.html', {'form': form})

            if CustomUser.objects.filter(username=email).exists():
                email_exists = True
                return render(request, 'core_website/cadastrar.html', {'form': form, 'email_exists': email_exists})

            if Enterprise.objects.filter(id_nacional=id_nacional).exists():
                id_nacional_exists = True
                return render(request, 'core_website/cadastrar.html', {'form': form, 'idnacional_exists': id_nacional_exists})

            enterprise = Enterprise.objects.create(
                tipo=tipo,
                nome=nome,
                id_nacional=id_nacional,
                telefone=telefone,
                email=email,
                senha=senha1
            )
            tenant = Tenant.objects.create(
                name=nome,
                client=enterprise
            )
            tenant.save() 

            user = CustomUser.objects.create_user(username=email, email=email, password=senha1, enterprise=enterprise, tenant=tenant, nome=nome)

            # Cria um domínio para o tenant
            domain = Domain.objects.create(
                domain=f'{tenant.schema_name}.neuron.com',
                tenant=tenant,
                is_primary=True
            )

            # Criar o schema
            with schema_context(tenant.schema_name):
                pass

            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('core_website:sucesso')
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = CadastroForm()

    return render(request, 'core_website/cadastrar.html', {'form': form, 'email_exists': email_exists, 'idnacional_exists': id_nacional_exists})

def sucesso(request):
    return render(request, 'core_website/cadastro_sucesso.html')

def apresentacao(request):
    return render(request, 'core_website/apresentacao.html')

def login(request):
    return render(request, 'core_website/login.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Use auth_login para evitar conflito de nome
            schema_name = user.tenant.schema_name
            redirect_url = reverse('sis_inicial:inicio', args=[schema_name])
            return redirect(redirect_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    # Defina o esquema para público antes de fazer logout
    connection.set_schema_to_public()
    auth_logout(request)
    return redirect(reverse('core_website:login'))