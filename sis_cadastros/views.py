from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@login_required(login_url='/accounts/login/')
def tb_fornecedor(request, schema_name):
    return render(request, 'sis_cadastros/tb_fornecedor.html')

@login_required(login_url='/accounts/login/')
def nv_fornecedor(request, schema_name):
    return render(request, 'sis_cadastros/nv_fornecedor.html')

@csrf_exempt
@login_required(login_url='/accounts/login/')
def cad_fornecedor(request, schema_name):
    if request.method == 'POST':
        print(request.POST)  # Imprime os dados do formulário no terminal

        cnpj = request.POST.get('cnpj')
        if cnpj:
            response = requests.get(f'https://www.receitaws.com.br/v1/cnpj/{cnpj}')
            data = response.json()
            return JsonResponse(data)

        return JsonResponse({"message": "Dados recebidos com sucesso!"})
    return JsonResponse({"message": "Método não permitido"}, status=405)