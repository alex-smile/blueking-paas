# Generated by Django 3.2.12 on 2022-06-22 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SceneTmpl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='名称')),
                ('display_name_zh_cn', models.CharField(blank=True, max_length=64, verbose_name='展示名称')),
                ('display_name_en', models.CharField(blank=True, max_length=64, verbose_name='展示名称')),
                ('description_zh_cn', models.CharField(blank=True, max_length=1024, verbose_name='描述')),
                ('description_en', models.CharField(blank=True, max_length=1024, verbose_name='描述')),
                ('enabled', models.BooleanField(default=True, verbose_name='是否启用')),
                ('tags', models.JSONField(blank=True, default=list, max_length=256, verbose_name='标签')),
                ('region', models.CharField(max_length=32, verbose_name='应用版本')),
                ('repo_url', models.CharField(blank=True, max_length=512, verbose_name='代码仓库地址')),
                ('blob_url', models.CharField(max_length=512, verbose_name='源码包地址（对象存储）')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
