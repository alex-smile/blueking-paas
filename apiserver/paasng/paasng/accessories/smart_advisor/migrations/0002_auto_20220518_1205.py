# Generated by Django 3.2.12 on 2022-05-18 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_advisor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentarylink',
            old_name='short_description',
            new_name='short_description_zh_cn'
        ),
        migrations.RenameField(
            model_name='documentarylink',
            old_name='title',
            new_name='title_zh_cn'
        ),
        migrations.AddField(
            model_name='documentarylink',
            name='short_description_en',
            field=models.CharField(blank=True, max_length=512, verbose_name='short_description'),
        ),
        migrations.AddField(
            model_name='documentarylink',
            name='title_en',
            field=models.CharField(default='', max_length=256, verbose_name='title'),
            preserve_default=False,
        ),
    ]
