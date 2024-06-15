#C:\Users\gusta\OneDrive\Área de Trabalho\Neuron_Hub\neuron_hub\core_website\middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django_tenants.middleware.main import TenantMainMiddleware
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import get_tenant_model, get_public_schema_name
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.db import connection
from django.conf import settings

class SessionTimeoutMiddleware(MiddlewareMixin):
    PUBLIC_URLS = [
        reverse('core_website:apresentacao'),
        reverse('core_website:cadastro_novo_negocio'),
        reverse('login'),
        reverse('core_website:login_sucesso'),
        reverse('core_website:sucesso'),
    ]

    def process_request(self, request):
        if request.path in self.PUBLIC_URLS:
            return None

        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

class CustomTenantMiddleware(TenantMainMiddleware):
    # Defina as URLs públicas que não requerem um schema_name
    PUBLIC_URLS = [
        '/',
        '/cadastrar-se/',
        '/accounts/login/',
        '/accounts/logout/',
        '/sucesso/',
        '/login/sucesso/'
    ]

    def process_request(self, request):
        path_parts = request.path_info.split('/')
        tenant_model = get_tenant_model()

        print(f"Request path: {request.path_info}")  # Log do caminho original

        # Verifique se a URL é pública
        if request.path in self.PUBLIC_URLS:
            connection.set_schema_to_public()
            print(f"Public URL accessed: {request.path}")  # Log para URLs públicas
        elif len(path_parts) > 2:
            schema_name = path_parts[1]
            try:
                tenant = tenant_model.objects.get(schema_name=schema_name)
                request.tenant = tenant
                connection.set_tenant(request.tenant)

                # Verificação adicional para o acesso ao dashboard
                if len(path_parts) > 3 and path_parts[2] == 'inicio' and path_parts[3] == 'begin':
                    if not request.user.is_authenticated:
                        return HttpResponseForbidden("You must be logged in to access this page")
                    
                    # Verifique se o usuário está acessando o esquema correto
                    if request.user.tenant.schema_name != schema_name:
                        return HttpResponseForbidden("You do not have permission to access this schema")

                print(f"Tenant schema: {schema_name}, Original path: {request.path_info}")  # Log do caminho ajustado
            except tenant_model.DoesNotExist:
                print(f"Tenant not found for schema: {schema_name}")  # Log para tenant não encontrado
                return HttpResponseNotFound("Tenant not found")
        else:
            connection.set_schema_to_public()
            print(f"Default schema accessed")  # Log para schema padrão

        response = self.get_response(request)
        return response
