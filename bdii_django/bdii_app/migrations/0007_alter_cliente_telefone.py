# Generated by Django 4.1.12 on 2023-12-17 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bdii_app', '0006_alter_cliente_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(max_length=15),
        ),
    ]