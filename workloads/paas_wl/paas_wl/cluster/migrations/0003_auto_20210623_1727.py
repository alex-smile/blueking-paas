# Generated by Django 2.2.17 on 2021-06-23 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0002_auto_20210524_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='cert_data',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='key_data',
            field=models.TextField(null=True),
        ),
    ]
