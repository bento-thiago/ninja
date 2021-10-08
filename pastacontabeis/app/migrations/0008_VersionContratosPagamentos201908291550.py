# Generated by Django 2.2.5 on 2020-02-18 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_VersionContratosPagamentos201908261122'),
    ]

    operations = [
        migrations.RunSQL("""
        ALTER TABLE contratos_pagamentos.contrato ADD dia_apropriacao int4 NOT NULL DEFAULT 1;
    """, ""),
        migrations.RunSQL("""
        ALTER TABLE contratos_pagamentos.contrato ADD CONSTRAINT contrato_dia_apropriacao_check CHECK(dia_apropriacao >= 1 AND dia_apropriacao <= 28);
    """, ""),
        migrations.RunSQL("""
        ALTER TABLE contratos_pagamentos.contrato ADD CONSTRAINT contrato_apropriacao_vencimento_check CHECK (dia_apropriacao <= dia_vencimento);
    """, ""),
    ]