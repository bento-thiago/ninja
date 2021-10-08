from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('diario_unico', '0062_Version202109150000'),
    ]
    #Refatorando os contratos para ter um Contrato que agrupa varias Ordens de Registro de Contrato
    operations = [
        migrations.RunSQL("""ALTER TABLE contratos DROP competencia_inicio;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE contratos DROP competencia_final;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE contratos DROP dia_processamento;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE contratos DROP tipo_recorrencia;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE contratos DROP tipo_cobranca;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE contratos DROP dia_vencimento;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE contratos DROP dias_antes_vencimento_para_desconto;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE contratos DROP dias_apos_vencimento_para_multa;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE contratos DROP dias_apos_vencimento_para_juros;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""alter table contratos drop index uk_contrato_codigo;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE contratos DROP codigo;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE contratos DROP descricao;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE contratos DROP participante_id;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE contratos DROP estabelecimento;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""alter table itens_contrato CHANGE  registro_contrato_id  registro_contrato_id;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""alter table contratos CHANGE  id  id_registro;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE itens_contrato ADD competencia_inicio date not null;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE itens_contrato ADD competencia_final date;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE itens_contrato ADD dia_processamento int  not null;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE itens_contrato ADD tipo_recorrencia varchar(40) not null ;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE itens_contrato ADD tipo_cobranca varchar(40) not null ;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE itens_contrato ADD dia_vencimento int  not null;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE itens_contrato ADD dias_antes_vencimento_para_desconto int not null;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE itens_contrato ADD dias_apos_vencimento_para_multa int not null;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE itens_contrato ADD dias_apos_vencimento_para_juros int not null;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE itens_contrato ADD situacao varchar(40) not null ;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE contratos ADD id_compartilhado varchar(36) not null;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""ALTER TABLE contratos rename to ordens_registro_contrato;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

        migrations.RunSQL("""create rowstore table contratos
                ( 
                    tenant int not null,
                    id_compartilhado varchar(36) not null,
                    codigo varchar(40)  not null,
                    participante_id varchar(36),
                    descricao varchar(200)  not null,
                    estabelecimento varchar(36), 
                    ultimo_registro varchar(36),          
                    SHARD KEY(tenant),
                    UNIQUE INDEX uk_contrato_codigo (tenant, codigo),
                    PRIMARY KEY (tenant, id_compartilhado)		
                );""", ""),  # Aqui ficaria o SQL para reverter a migration),

    ]
