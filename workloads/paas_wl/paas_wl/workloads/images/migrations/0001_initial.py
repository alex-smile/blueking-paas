# Generated by Django 2.2.17 on 2022-01-24 02:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0007_config_runtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppImageCredential',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('registry', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=255)),
                ('app', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='api.App')),
            ],
            options={
                'unique_together': {('app', 'registry')},
            },
        ),
    ]
