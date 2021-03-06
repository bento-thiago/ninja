# Generated by Django 2.2.5 on 2020-01-06 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0029_Version201908141212'),
    ]

    operations = [

        migrations.RunSQL("""
            delete from definicoes_lancamentos;""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),



        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('23cd7e1f-2af9-09a9-50a1b7db20fab182', 'PREVISAO_CONTA_GAS', 1, 'D', 1, '4.1.1.08.0003', 'Despesa com conta de gas', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('3764f175-8cd9-4721-bf8e-b3b79b810b8f', 'PAGAMENTO_CONTA_AGUA', 1, 'D', 1, '2.1.2.04', 'Pagamento de conta de agua', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('15f19dd1-09da-d2d8-b021a2b6648213d0', 'PREVISAO_CONTA_AGUA', 1, 'C', 2, '2.1.2.04', 'Conta de agua a pagar', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('617ae1ce-99e9-3c29-9c187d71baa9e1d3', 'PREVISAO_CONTA_ENERGIA', 1, 'D', 1, '4.1.1.08.0002', 'Despesa com conta de energia eletrica', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('63ce1947-342f-f448-215173497d8c9ae3', 'PREVISAO_CONTA_GAS', 1, 'C', 2, '2.1.2.04', 'Conta de gas a pagar', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('7a84bd47-5f04-9dd9-2c28f1feab27403e', 'APROPRIACAO_CONTA_GAS', 2, 'C', 2, '1.1.1.01', 'Pagamento de conta de gas', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('96edffba-1194-438c-92f8-c800083aee76', 'PAGAMENTO_CONTA_ENERGIA', 1, 'D', 1, '2.1.2.04', 'Pagamento de conta de energia eletrica', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('b8530527-254b-c8ca-f0ad0f630b5df9fe', 'APROPRIACAO_CONTA_AGUA', 2, 'D', 1, '2.1.2.04', 'Pagamento de conta de agua', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('c4af4892-fac3-95a5-8176a500811e0ab6', 'PREVISAO_CONTA_GAS', 2, 'D', 1, '2.1.2.04', 'Pagamento de conta de gas', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('0150c355-1313-2fe0-54838e46d3a1f278', 'PREVISAO_COTA_CONDOMINIAL', 1, 'D', 1, '1.1.2.01', 'Cotas condominiais a receber', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('072f1bb3-f895-5a95-75d890b273edf2d5', 'APROPRIACAO_CONTA_ENERGIA', 2, 'C', 2, '1.1.1.01', 'Pagamento de conta de energia eletrica', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('2687a138-bb36-44ce-9e1b-2858fa73c773', 'PAGAMENTO_COTA_CONDOMINIAL', 1, 'D', 1, '1.1.2.01', 'Recebimento de pagamento de cota condominial', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('bea13e66-72b6-1a60-9b0d54e26cfdbd70', 'APROPRIACAO_CONTA_AGUA', 2, 'C', 2, '1.1.1.01', 'Pagamento de conta de agua', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('e53aeafd-2492-4c51-98f6-51c423785c24', 'APROPRIACAO_CONTA_GAS', 1, 'C', 2, '2.1.2.04', 'Conta de gas a pagar', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('30c71711-0656-3663-2a681d5d3705335e', 'PREVISAO_CONTA_ENERGIA', 2, 'D', 1, '2.1.2.04', 'Pagamento de conta de energia eletrica', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('3ea9642b-6f69-4706-bae3b8cc663799a5', 'PREVISAO_CONTA_GAS', 2, 'C', 2, '1.1.1.01', 'Pagamento de conta de gas', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('4d110a75-9b36-4106-b05e-7ae25f3edc65', 'PAGAMENTO_CONTA_ENERGIA', 1, 'C', 2, '1.1.1.01', 'Pagamento de conta de energia eletrica', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('7cc91f9d-e92c-be47-7fceffb51b5fb557', 'APROPRIACAO_CONTA_GAS', 2, 'D', 1, '2.1.2.04', 'Pagamento de conta de gas', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('a93223e6-ec8e-2388-eac9c0454101a269', 'PREVISAO_COTA_CONDOMINIAL', 1, 'C', 2, '3.1.1.01', 'Receita de cotas condominiais', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('aa2f144c-5efe-c0c2-2f235950016e453d', 'PREVISAO_CONTA_AGUA', 2, 'C', 2, '1.1.1.01', 'Pagamento de conta de agua', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('d59bde3d-2594-47c6-a156-a66fb17983d3', 'APROPRIACAO_CONTA_ENERGIA', 1, 'C', 2, '2.1.2.04', 'Conta de energia eletrica a pagar', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('d7052ac5-ba0d-4ba1-8973-f528442e061b', 'PAGAMENTO_CONTA_GAS', 1, 'C', 2, '1.1.1.01', 'Pagamento de conta de gas', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('c9caeac5-f3fc-ceab-c09725567736235b', 'PREVISAO_COTA_CONDOMINIAL', 2, 'C', 2, '1.1.1.01', 'Recebimento de pagamento de cota condominial', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('f553cc7f-593e-4499-aaf4-934138a0b060', 'APROPRIACAO_CONTA_AGUA', 1, 'C', 2, '2.1.2.04', 'Conta de agua a pagar', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('0f937f05-f762-4d58-8d1e-a5bdc3b5edaa', 'PAGAMENTO_CONTA_GAS', 1, 'D', 1, '2.1.2.04', 'Pagamento de conta de gas', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('331e4e3f-1ca8-3150-9b23f76cb6b40fb7', 'PREVISAO_CONTA_ENERGIA', 1, 'C', 2, '2.1.2.04', 'Conta de energia eletrica a pagar', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('368af54b-5b21-4231-91d5-a36e6b1b0ac6', 'APROPRIACAO_CONTA_ENERGIA', 1, 'D', 1, '4.1.1.08.0002', 'Despesa com conta de energia eletrica', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('39ebc9eb-40a7-43ce-bf04-044f9e27ba6c', 'PAGAMENTO_CONTA_AGUA', 1, 'C', 2, '1.1.1.01', 'Pagamento de conta de agua', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('45d4b379-6201-ef28-de8dafbb48d7ab67', 'PREVISAO_CONTA_ENERGIA', 2, 'C', 2, '1.1.1.01', 'Pagamento de conta de energia eletrica', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('d80d0fee-4ab7-4100-b593-2cd4687cc98a', 'PAGAMENTO_COTA_CONDOMINIAL', 1, 'C', 2, '1.1.1.01', 'Recebimento de pagamento de cota condominial', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('06f45ed4-86b2-e330-d62417186c301870', 'PREVISAO_COTA_CONDOMINIAL', 2, 'D', 1, '1.1.2.01', 'Recebimento de pagamento de cota condominial', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('23dcdb37-b66c-47f4-b94d-c2709c3e1028', 'APROPRIACAO_COTA_CONDOMINIAL', 1, 'D', 1, '1.1.2.01', 'Cotas condominiais a receber', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('7dfbc813-060f-5c0d-4d835e73eb990f6a', 'APROPRIACAO_CONTA_ENERGIA', 2, 'D', 1, '2.1.2.04', 'Pagamento de conta de energia eletrica', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('091dddc6-f3cd-10ef-5729a7f19ff39613', 'APROPRIACAO_COTA_CONDOMINIAL', 2, 'D', 1, '1.1.2.01', 'Recebimento de pagamento de cota condominial', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('2ba5b3dd-56d7-464c-b848-3837a1742012', 'APROPRIACAO_CONTA_GAS', 1, 'D', 1, '4.1.1.08.0003', 'Despesa com conta de gas', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('5161dd41-9153-4c72-8f55-d5021a8f0596', 'APROPRIACAO_COTA_CONDOMINIAL', 1, 'C', 2, '3.1.1.01', 'Receita de cotas condominiais', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('5d3d9a92-c6a4-46a3-9a32-7794c774acf3', 'APROPRIACAO_CONTA_AGUA', 1, 'D', 1, '4.1.1.07.0001', 'Despesa com conta de agua', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 3, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('7aba0877-0ed9-407b-f59076ae54ccea2f', 'APROPRIACAO_COTA_CONDOMINIAL', 2, 'C', 2, '1.1.1.01', 'Recebimento de pagamento de cota condominial', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('a8da17ba-24ca-5b04-e1a8f398b2ac6ccd', 'PREVISAO_CONTA_AGUA', 1, 'D', 1, '4.1.1.07.0001', 'Despesa com conta de agua', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_apropriacao');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""INSERT INTO definicoes_lancamentos
            (definicao_lancamento, evento, numero, natureza, ordem, conta, historico, formula, diario_subtipo, empresa, ano, plano_contas, tenant, situacao, formula_data)
            VALUES('da1a4b7b-f6e4-3b22-be46b7afc86d37b9', 'PREVISAO_CONTA_AGUA', 2, 'D', 1, '2.1.2.04', 'Pagamento de conta de agua', 'valor', 1, NULL, NULL, 'CONDOMINIO', 47, 2, 'data_pagamento');""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
    ]
