# Generated by Django 2.2.5 on 2020-02-18 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_VersionGuias201912051712'),
    ]

    operations = [
        migrations.RunSQL("""CREATE SCHEMA IF NOT EXISTS util;""", ""),

        migrations.RunSQL("""CREATE TABLE util.log_assincrono(
            token varchar(60) NOT NULL,
            datahora date NOT NULL,
            recurso varchar(60) NOT NULL,
            status varchar(500) NOT NULL,
            tenant bigint NOT NULL,
            CONSTRAINT requisicoes_pk PRIMARY KEY(token, datahora, status)
        )
            """, ""),
    ]