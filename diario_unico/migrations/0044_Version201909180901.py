# Generated by Django 2.2.5 on 2020-01-06 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario_unico', '0043_Version201909180900'),
    ]

    operations = [
        migrations.RunSQL("""update  conta_contabil
            set natureza='D'
            where codigo like '4%'""",  ""  # Aqui ficaria o SQL para reverter a migration
                          ),
    ]
