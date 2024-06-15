from django.core.management.base import BaseCommand, CommandError
from django_tenants.utils import get_tenant_model
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Reverts migrations for all tenants and the public schema for a specific app'

    def add_arguments(self, parser):
        parser.add_argument('app', type=str, help='The name of the app to revert migrations for')
        parser.add_argument('migration', type=str, help='The migration name or number to revert to (e.g., zero, 0002)')

    def handle(self, *args, **options):
        app_name = options['app']
        migration_name = options['migration']
        
        if not app_name:
            raise CommandError('App name must be provided')
        
        if not migration_name:
            raise CommandError('Migration name or number must be provided')

        TenantModel = get_tenant_model()
        tenants = TenantModel.objects.all()

        # Reverter migrações para o schema público
        self.stdout.write(self.style.NOTICE(f'Reverting migrations for public schema for app {app_name} to {migration_name}'))
        call_command('migrate_schemas', schema_name='public', app_label=app_name, migration_name=migration_name)

        # Reverter migrações para cada tenant
        for tenant in tenants:
            self.stdout.write(self.style.NOTICE(f'Reverting migrations for tenant: {tenant.schema_name} for app {app_name} to {migration_name}'))
            call_command('migrate_schemas', schema_name=tenant.schema_name, app_label=app_name, migration_name=migration_name)

        self.stdout.write(self.style.SUCCESS(f'Successfully reverted migrations for all tenants and the public schema for app {app_name} to {migration_name}'))
