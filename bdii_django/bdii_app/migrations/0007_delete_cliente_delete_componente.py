# Generated by Django 4.1.12 on 2023-12-19 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdii_app', '0006_alter_cliente_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cliente',
        ),
        migrations.DeleteModel(
            name='Componente',
        ),
    ]
