# Generated by Django 2.2.5 on 2020-01-06 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0028_Version201908121636'),
    ]

    operations = [
        migrations.RunSQL("""
            ALTER TABLE definicoes_lancamentos ADD situacao INT DEFAULT 0 NOT NULL;""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),

        migrations.RunSQL("""
            ALTER TABLE definicoes_lancamentos ADD formula_data varchar(100) NULL;""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),


        migrations.RunSQL("""
            CREATE TABLE definicoes_info_pagamento (
                evento varchar(100) NOT NULL,
                numero_lancamento varchar(100) NULL,
                formula_vencimento varchar(100) NOT NULL,
                situacao int NOT NULL
            );""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),


        migrations.RunSQL("""
            CREATE TABLE definicoes_info_cobranca (
                evento varchar(100) NOT NULL,
                numero_lancamento INT NOT NULL,
                formula_juros_mensal VARCHAR(100) NOT NULL,
                formula_multa_atraso varchar(100) NOT NULL,
                formula_desconto varchar(100) NOT NULL,
                formula_texto_instrucao varchar(100) NOT NULL,
                formula_vencimento varchar(100) NOT NULL,
                formula_participante varchar(100) NOT NULL,
                situacao int NOT NULL
            );""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),


        migrations.RunSQL("""
            ALTER TABLE enderecos ADD estado varchar(100) NULL;""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),


        migrations.RunSQL("""
            INSERT INTO enderecos
                (cidade, bairro, cep, tipologradouro, logradouro, numero, complemento, pessoa, cobranca)
                VALUES('Casimiro de Abreu', 'Centro', '28860000', '0', 'Rua Principal', '521', NULL, '63f7d155-ce46-492e-9aea-9bf7b5bb42ed', 1);""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),


        migrations.RunSQL("""
            INSERT INTO definicoes_info_cobranca
            (evento, numero_lancamento, formula_juros_mensal, formula_multa_atraso, formula_desconto, formula_texto_instrucao, formula_vencimento, formula_participante, situacao)
            VALUES('PAGAMENTO_COTA_CONDOMINIAL', 1, 'juros_mensal', 'multa_atraso', 'desconto', 'texto_instrucao', 'data_pagamento', 'participante', 4);
            INSERT INTO definicoes_info_cobranca
            (evento, numero_lancamento, formula_juros_mensal, formula_multa_atraso, formula_desconto, formula_texto_instrucao, formula_vencimento, formula_participante, situacao)
            VALUES('APROPRIACAO_COTA_CONDOMINIAL', 2, 'juros_mensal', 'multa_atraso', 'desconto', 'texto_instrucao', 'data_pagamento', 'participante', 1);            
            """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),



        migrations.RunSQL("""
            INSERT INTO definicoes_info_pagamento
            (evento, numero_lancamento, formula_vencimento, situacao)
            VALUES('APROPRIACAO_CONTA_AGUA', '2', 'data_pagamento', 1);
            INSERT INTO definicoes_info_pagamento
            (evento, numero_lancamento, formula_vencimento, situacao)
            VALUES('APROPRIACAO_CONTA_ENERGIA', '2', 'data_pagamento', 1);
            INSERT INTO definicoes_info_pagamento
            (evento, numero_lancamento, formula_vencimento, situacao)
            VALUES('PAGAMENTO_CONTA_AGUA', '1', 'data_pagamento', 3);
            INSERT INTO definicoes_info_pagamento
            (evento, numero_lancamento, formula_vencimento, situacao)
            VALUES('PAGAMENTO_CONTA_ENERGIA', '1', 'data_pagamento', 3);
            INSERT INTO definicoes_info_pagamento
            (evento, numero_lancamento, formula_vencimento, situacao)
            VALUES('PAGAMENTO_CONTA_GAS', '1', 'data_pagamento', 3);
            INSERT INTO definicoes_info_pagamento
            (evento, numero_lancamento, formula_vencimento, situacao)
            VALUES('APROPRIACAO_CONTA_GAS', '2', 'data_pagamento', 1);
            """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
    ]
