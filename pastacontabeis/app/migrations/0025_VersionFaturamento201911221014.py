# Generated by Django 2.2.5 on 2020-02-18 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_VersionFaturamento201910251614'),
    ]

    operations = [
        migrations.RunSQL("""CREATE SCHEMA financeiro;""", ""),

        migrations.RunSQL("""CREATE TABLE financeiro.conta_financeira(
            iban varchar(60) NOT NULL,
            banco int4 NOT NULL,
            agencia int4 NOT NULL,
            conta int4 NOT NULL,
            digito int4 NOT NULL,
            cpf_cnpj varchar(18) NOT NULL,
            api_key json NOT NULL,
            padrao bool NULL,
            tenant int8 NOT NULL,
            CONSTRAINT conta_financeira_pk PRIMARY KEY(iban)
        )
            """, ""),

        migrations.RunSQL("""CREATE TABLE financeiro.conta_estabelecimento (
            conta_estabelecimento uuid NOT NULL DEFAULT uuid_generate_v4(),
            conta_financeira varchar(60) NOT NULL,
            estabelecimento varchar(60) NULL,
            CONSTRAINT conta_estabelecimento_pkey PRIMARY KEY (conta_estabelecimento),
            CONSTRAINT conta_financeira_fk FOREIGN KEY (conta_financeira) REFERENCES financeiro.conta_financeira(iban) ON UPDATE CASCADE ON DELETE CASCADE
            );""", ""),

        migrations.RunSQL("""CREATE INDEX fki_conta_estabelecimento_fk ON financeiro.conta_estabelecimento USING btree(conta_financeira)
                          """, ""),
    ]