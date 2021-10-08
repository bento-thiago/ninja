from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0061_Version202109140000'),
    ]

    operations = [
        migrations.RunSQL("""ALTER TABLE pessoas_registros ADD endereco_cobranca varchar(36) NULL;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE pessoas_registros ADD endereco_principal varchar(36) NULL;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE pessoas_registros ADD contato_cobranca varchar(36) NULL;""",
                          ""),  # Aqui ficaria o SQL para reverter a migration),
        migrations.RunSQL("""ALTER TABLE pessoas_registros ADD contato_principal varchar(36) NULL;""",
                          "")
    ]
