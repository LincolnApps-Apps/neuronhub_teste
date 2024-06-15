# core_tenants/models.py

from django_tenants.models import TenantMixin, DomainMixin
from django.db import models
from core_cadastros.models import Enterprise
import string

class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    client = models.OneToOneField(Enterprise, on_delete=models.CASCADE, related_name='tenant')
    schema_name = models.CharField(max_length=63, unique=True)
    auto_create_schema = True

    def save(self, *args, **kwargs):
        if not self.schema_name:
            self.schema_name = self.generate_schema_name()
        super().save(*args, **kwargs)

    def generate_schema_name(self):
        prefix = "neurondb."
        for letter in string.ascii_uppercase:
            for number in range(1, 100):
                schema_name = f"{prefix}{number:02d}{letter}"
                if not Tenant.objects.filter(schema_name=schema_name).exists():
                    return schema_name
        raise ValueError("Excedeu o limite de schemas possíveis.")

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    pass
