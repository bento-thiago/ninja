# Generated by Django 2.2.5 on 2020-01-03 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0015_Version201907160737'),
    ]

    operations = [

        migrations.RunSQL("""
                alter table diario_unico drop column percentagem_sobre_base
            """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),

        migrations.RunSQL("""
               alter table diario_unico add column percentagem_sobre_base decimal(16,8);
            """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),

        migrations.RunSQL("""
                alter table diario_unico drop column valor;
            """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),

        migrations.RunSQL("""
                alter table diario_unico add column valor decimal(16, 8);
            """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),

    ]