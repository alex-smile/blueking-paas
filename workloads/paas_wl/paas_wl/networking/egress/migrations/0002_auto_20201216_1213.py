# Generated by Django 2.2.17 on 2020-12-16 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rcstateappbinding',
            name='app',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.App'),
        ),
        migrations.AlterUniqueTogether(
            name='rcstateappbinding',
            unique_together=set(),
        ),
    ]
