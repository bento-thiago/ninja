# Generated by Django 2.2.5 on 2020-02-18 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_VersionFaturamento201911221014'),
    ]

    operations = [
        migrations.RunSQL(
            """alter table faturamento.contrato drop column codigo_transacao;""", ""),
    ]