# Generated by Django 4.2.13 on 2024-06-15 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_cadastros', '0004_customuser_tenant'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='nome',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
