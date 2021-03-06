# Generated by Django 2.2.5 on 2020-01-06 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0022_Version201908010901'),
    ]

    operations = [
        migrations.RunSQL("""
                insert into definicoes_lancamentos(definicao_lancamento,
                                            evento,
                                            numero,
                                            natureza,
                                            ordem,
                                            conta,
                                            historico,
                                            formula,
                                            diario_subtipo,
                                            plano_contas)
                values ('96edffba-1194-438c-92f8-c800083aee76',
                        'PAGAMENTO_CONTA_ENERGIA',
                        1,
                        'D',
                        1,
                        '2.1.2.04',
                        'Pagamento de conta de energia eletrica',
                        'valor',
                        1,
                        'CONDOMINIO');
                """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),


        migrations.RunSQL("""
                insert into definicoes_lancamentos(definicao_lancamento,
                                            evento,
                                            numero,
                                            natureza,
                                            ordem,
                                            conta,
                                            historico,
                                            formula,
                                            diario_subtipo,
                                            plano_contas)
                values ('4d110a75-9b36-4106-b05e-7ae25f3edc65',
                        'PAGAMENTO_CONTA_ENERGIA',
                        1,
                        'C',
                        2,
                        '1.1.1.01',
                        'Pagamento de conta de energia eletrica',
                        'valor',
                        1,
                        'CONDOMINIO');
                """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),


        migrations.RunSQL("""
                insert into definicoes_lancamentos(definicao_lancamento,
                                            evento,
                                            numero,
                                            natureza,
                                            ordem,
                                            conta,
                                            historico,
                                            formula,
                                            diario_subtipo,
                                            plano_contas)
                values ('3764f175-8cd9-4721-bf8e-b3b79b810b8f',
                        'PAGAMENTO_CONTA_AGUA',
                        1,
                        'D',
                        1,
                        '2.1.2.04',
                        'Pagamento de conta de agua',
                        'valor',
                        1,
                        'CONDOMINIO');
                """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),



        migrations.RunSQL("""
                insert into definicoes_lancamentos(definicao_lancamento,
                                            evento,
                                            numero,
                                            natureza,
                                            ordem,
                                            conta,
                                            historico,
                                            formula,
                                            diario_subtipo,
                                            plano_contas)
                values ('39ebc9eb-40a7-43ce-bf04-044f9e27ba6c',
                        'PAGAMENTO_CONTA_AGUA',
                        1,
                        'C',
                        2,
                        '1.1.1.01',
                        'Pagamento de conta de agua',
                        'valor',
                        1,
                        'CONDOMINIO');
                """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),



        migrations.RunSQL("""
                insert into definicoes_lancamentos(definicao_lancamento,
                                            evento,
                                            numero,
                                            natureza,
                                            ordem,
                                            conta,
                                            historico,
                                            formula,
                                            diario_subtipo,
                                            plano_contas)
                values ('0f937f05-f762-4d58-8d1e-a5bdc3b5edaa',
                        'PAGAMENTO_CONTA_GAS',
                        1,
                        'D',
                        1,
                        '2.1.2.04',
                        'Pagamento de conta de gas',
                        'valor',
                        1,
                        'CONDOMINIO');
                """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),




        migrations.RunSQL("""
                insert into definicoes_lancamentos(definicao_lancamento,
                                            evento,
                                            numero,
                                            natureza,
                                            ordem,
                                            conta,
                                            historico,
                                            formula,
                                            diario_subtipo,
                                            plano_contas)
                values ('d7052ac5-ba0d-4ba1-8973-f528442e061b',
                        'PAGAMENTO_CONTA_GAS',
                        1,
                        'C',
                        2,
                        '1.1.1.01',
                        'Pagamento de conta de gas',
                        'valor',
                        1,
                        'CONDOMINIO');
                """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),


        migrations.RunSQL("""
                insert into definicoes_lancamentos(definicao_lancamento,
                                            evento,
                                            numero,
                                            natureza,
                                            ordem,
                                            conta,
                                            historico,
                                            formula,
                                            diario_subtipo,
                                            plano_contas)
                values ('2687a138-bb36-44ce-9e1b-2858fa73c773',
                        'PAGAMENTO_COTA_CONDOMINIAL',
                        1,
                        'D',
                        1,
                        '1.1.2.01',
                        'Recebimento de pagamento de cota condominial',
                        'valor',
                        1,
                        'CONDOMINIO');
                """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),


        migrations.RunSQL("""
                insert into definicoes_lancamentos(definicao_lancamento,
                                            evento,
                                            numero,
                                            natureza,
                                            ordem,
                                            conta,
                                            historico,
                                            formula,
                                            diario_subtipo,
                                            plano_contas)
                values ('d80d0fee-4ab7-4100-b593-2cd4687cc98a',
                        'PAGAMENTO_COTA_CONDOMINIAL',
                        1,
                        'C',
                        2,
                        '1.1.1.01',
                        'Recebimento de pagamento de cota condominial',
                        'valor',
                        1,
                        'CONDOMINIO');
                """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
    ]
