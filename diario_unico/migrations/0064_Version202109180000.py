from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('diario_unico', '0063_Version202109160000'),
    ]
    # Refatorando os contratos para ter um Contrato que agrupa varias Ordens de Registro de Contrato
    operations = [

        migrations.RunSQL("""ALTER TABLE contatos ADD email varchar(200);""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE itens_contrato change aliquota_pis aliquota_pis;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE pessoas_registros add contrato_id varchar(36);""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),

    ]
