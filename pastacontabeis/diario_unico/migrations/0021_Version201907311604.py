# Generated by Django 2.2.5 on 2020-01-06 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0020_Version201907311356'),
    ]

    operations = [
        migrations.RunSQL("""
                alter table documento drop column numero_contrato;
             """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
    ]