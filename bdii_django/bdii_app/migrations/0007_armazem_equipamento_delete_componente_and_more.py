# Generated by Django 4.1.12 on 2023-12-19 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bdii_app', '0006_alter_cliente_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Armazem',
            fields=[
                ('id_armazem', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
                ('quantidade_em_stock', models.IntegerField()),
                ('data_entrada', models.DateTimeField(auto_now_add=True)),
                ('data_saida', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Armazem',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('ID_equipamento', models.AutoField(primary_key=True, serialize=False)),
                ('Tipo', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
                ('valor_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'Equipamento',
            },
        ),
        migrations.DeleteModel(
            name='Componente',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(max_length=15),
        ),
        migrations.CreateModel(
            name='EquipamentoArmazenamento',
            fields=[
                ('equipamentoID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='bdii_app.equipamento')),
                ('pronto_para_armazenar', models.BooleanField()),
                ('id_armazem', models.ForeignKey(db_column='id_armazem', on_delete=django.db.models.deletion.CASCADE, to='bdii_app.armazem')),
            ],
            options={
                'db_table': 'equipamentoArmazenamento',
            },
        ),
    ]
