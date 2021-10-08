from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('diario_unico', '0065_Version202109260000'),
    ]
    # Refatorando os contratos para ter um Contrato que agrupa varias Ordens de Registro de Contrato
    operations = [

        migrations.RunSQL("""drop table info_cobranca;;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""create rowstore table infos_cobranca (
            id varchar(36) not null,
            vencimento date,
            data_limite_desconto date,
            data_inicio_multa date,
            percentual_desconto numeric(20,4),
            percentual_multa numeric(20,4),
            percentual_juros_diario numeric(20,4),
            valor_bruto numeric(20,2),
            valor_liquido numeric(20,2),
            texto_instrucao varchar(200),
            situacao varchar(60),
            cpf_cnpj_cliente varchar(14),
            nome_cliente varchar(400),
            documento_id varchar(36) not null,
            numero int,
            nosso_numero varchar(20),
            endereco_cidade varchar(7),
            email varchar(100) ,
            tenant int not null,
            PRIMARY KEY (tenant, id),		
            SHARD KEY(tenant)		
        )
                );
        """, ""),  # Aqui ficaria o SQL para reverter a migration),

    ]
