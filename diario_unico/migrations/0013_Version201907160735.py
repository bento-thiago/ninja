# Generated by Django 2.2.5 on 2020-01-03 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0012_Version201907160734'),
    ]

    operations = [

        migrations.RunSQL("""
                alter table diario_universal rename to diario_unico;
            """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),

        migrations.RunSQL("""
                alter table diario_unico add column diario_unico varchar(36) not null;
            """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),

        migrations.RunSQL("""
               update diario_unico set diario_unico=diario_universal;
            """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),

        migrations.RunSQL("""
                alter table diario_unico drop column diario_universal;
            """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),



    ]