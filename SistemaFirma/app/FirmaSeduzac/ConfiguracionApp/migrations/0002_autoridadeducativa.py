# Generated by Django 5.0.6 on 2024-06-20 18:17

import ConfiguracionApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConfiguracionApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoridadEducativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_autoridad', models.CharField(default='MARIBEL VILLALPANDO HARO. SECRETARIA DE EDUCACIÓN DEL ESTADO DE ZACATECAS.', max_length=100)),
                ('certificado_autoridad', models.CharField(default='00000000000000008682', max_length=20, validators=[ConfiguracionApp.models.validate_certificado_autoridad])),
            ],
        ),
    ]
