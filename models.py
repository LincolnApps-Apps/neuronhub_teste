from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps

class Enterprise(models.Model):
    tipo = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    id_nacional = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    senha = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class CustomUser(AbstractUser):
    enterprise = models.OneToOneField(Enterprise, on_delete=models.CASCADE, null=True, blank=True)
    tenant = models.ForeignKey('core_tenants.Tenant', on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_tenant(self):
        Tenant = apps.get_model('core_tenants', 'Tenant')
        return Tenant.objects.get(id=self.tenant_id)
