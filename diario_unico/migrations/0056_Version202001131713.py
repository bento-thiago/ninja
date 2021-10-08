# Generated by Django 2.2.5 on 2020-01-13 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0055_Version202001091334'),
    ]

    operations = [
        migrations.RunSQL("""ALTER TABLE documento DROP COLUMN tipo;""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""ALTER TABLE diario_unico DROP COLUMN diario_unico_tipo;""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""ALTER TABLE documento ADD tipo varchar(40) NULL;""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
        migrations.RunSQL("""ALTER TABLE diario_unico ADD diario_unico_tipo varchar(40) NULL;""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),

    ]