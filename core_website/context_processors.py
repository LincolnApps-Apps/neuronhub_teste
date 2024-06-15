# core_website/context_processors.py

def tenant_schema(request):
    return {
        'tenant_schema': request.tenant.schema_name if hasattr(request, 'tenant') else None
    }