# Generated by Django 2.2.5 on 2020-01-06 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0034_Version201908230916'),
    ]

    operations = [
        migrations.RunSQL("""
        update enderecos set pessoa='3e5bda63-1b17-47a0-be51-842539357ebe'
    """,  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
    ]
