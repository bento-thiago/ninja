from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0060_Version202003311650'),
    ]

    operations = [
        migrations.RunSQL("""drop table pessoas""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""create rowstore table pessoas 
            ( 
                tenant int not null,
                id_compartilhado varchar(36) not null,
                codigo varchar(40) not null,
                registro_principal varchar(36),
                SHARD KEY(tenant),
                PRIMARY KEY (tenant, id_compartilhado),
                UNIQUE INDEX uk_pessoas_codigo (tenant, codigo),
                UNIQUE INDEX uk_pessoas_registro (tenant, registro_principal)
            );""",""),  # Aqui ficaria o SQL para reverter a migration),
        
        migrations.RunSQL("""create rowstore table pessoas_registros 
            ( 
                tenant int not null,
                id_compartilhado varchar(36) not null,
                id_registro varchar(36) not null,
                cpf_cnpj varchar(14) not null,
                nome_fantasia varchar(200) not null,
                razao_social varchar(200) not null,
                qualificacao varchar(70) not null,
                inscricao_municipal varchar(40),
                inscricao_estadual varchar(40),
                origem_informacoes varchar(30),
                tipo_simples_nacional varchar(30),
                registro_papel varchar(30),
                SHARD KEY(tenant),
                PRIMARY KEY (tenant, id_registro)		
            );""",""),  # Aqui ficaria o SQL para reverter a migration),
        
        migrations.RunSQL("""drop table enderecos;""",""),  # Aqui ficaria o SQL para reverter a migration),
         
        migrations.RunSQL("""create rowstore table enderecos
            ( 
                tenant int not null,
                id varchar(36) not null,
                pessoa_registro varchar(36) not null,
                tipo_logradouro varchar(10) not null,
                cidade_ibge varchar(7) not null,
                logradouro varchar(100) not null,
                numero varchar(10) not null,
                complemento varchar(100) not null,
                bairro varchar(100) not null,
                cep varchar(8) not null,
                uf varchar(2) not null,
                pais_codigo varchar(4) not null,
                referencia varchar(100),
                SHARD KEY(tenant),
                PRIMARY KEY (tenant, id)		
            );""",""),  # Aqui ficaria o SQL para reverter a migration),
         
         
        migrations.RunSQL("""create rowstore table contatos
            ( 
                tenant int not null,
                id varchar(36) not null,
                pessoa_registro varchar(36) not null,
                nome_ou_descricao varchar(100) ,
                telefone varchar(30),		
                SHARD KEY(tenant),
                PRIMARY KEY (tenant, id)		
            );""",""),  # Aqui ficaria o SQL para reverter a migration),
         

        migrations.RunSQL("""create rowstore table contratos
            ( 
                tenant int not null,
                id varchar(36) not null,
                codigo varchar(40)  not null,
                descricao varchar(200)  not null,
                data_registro TIMESTAMP   not null,
                participante_id varchar(36) not null ,
                estabelecimento varchar(36) not null ,
                competencia_inicio date not null ,
                competencia_final date ,
                dia_processamento int  not null,
                tipo_recorrencia varchar(40) not null ,
                tipo_cobranca varchar(40) not null ,
                dia_vencimento int  not null,
                dias_antes_vencimento_para_desconto int not null,
                dias_apos_vencimento_para_multa int not null ,
                dias_apos_vencimento_para_juros int not null,
                SHARD KEY(tenant),
                UNIQUE INDEX uk_contrato_codigo (tenant, codigo),
                PRIMARY KEY (tenant, id)		
            );""",""),  # Aqui ficaria o SQL para reverter a migration),
        
        migrations.RunSQL("""create rowstore table itens_contrato
            ( 
                tenant int not null,
                id varchar(36) not null,
                id_servico varchar(36)  not null,
                registro_contrato_id varchar(36) not null,
                valor_unitario numeric(20,2)  not null,
                quantidade numeric(20,4)   not null,
                valor_total numeric(20,2) not null ,
                recorrente boolean not null ,
                codigo_item_contrato varchar(40) not null ,
                codigo_servico varchar(40) not null ,
                descricao varchar(200)  not null,
                incidencia_inss numeric(20,2) not null ,
                aliquota_inss numeric(20,2) not null ,
                aliquota_ir numeric(20,2) not null ,
                aliquota_pis numeric(20,2) not null ,
                aliquota_cofins numeric(20,2) not null ,
                aliquota_csll numeric(20,2) not null ,
                SHARD KEY(tenant),
                UNIQUE INDEX uk_contrato_codigo (tenant, registro_contrato_id, codigo_item_contrato),
                PRIMARY KEY (tenant, id)		
            ); """,""),  # Aqui ficaria o SQL para reverter a migration),
    ]
