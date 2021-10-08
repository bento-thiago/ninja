# Generated by Django 2.2.5 on 2020-01-06 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0025_Version201908081130'),
    ]

    operations = [
        migrations.RunSQL("""
                CREATE TABLE info_cobranca(
                         info_cobranca varchar(36) not null,
                         documento varchar(30) not null,
                         juros_mensal numeric(20, 4),
                         multa_atraso numeric(20, 4),
                         desconto numeric(20, 4),
                         texto_instrucao varchar(528),
                         numero int not null,
                         nosso_numero varchar(20),
                         id_externo varchar(20),
                         banco_numero varchar(3),
                         uuid_externo varchar(36),
                         url_boleto varchar(500),
                         linha_digitavel varchar(60),
                         tentativas_registro int default 0,
                         vencimento date not null,
                         situacao int default 0,
                         mensagem_erro varchar(200),
                         tenant bigint
                     )
                     ENGINE=InnoDB;
            """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
    ]