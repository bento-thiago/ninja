# Generated by Django 2.2.5 on 2020-02-18 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_VersionFaturamento201908011425'),
    ]

    operations = [
        migrations.RunSQL("""
      alter table faturamento.contrato_participante add column email character varying(160);
    """, ""),
    ]
