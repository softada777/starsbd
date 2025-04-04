# Generated by Django 5.1.6 on 2025-03-31 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterModelOptions(
            name='star',
            options={'ordering': ['-time_create'], 'verbose_name': 'Знаменитость', 'verbose_name_plural': 'Знаменитости'},
        ),
        migrations.RemoveField(
            model_name='star',
            name='categories',
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, verbose_name='URL'),
        ),
        migrations.AddField(
            model_name='country',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, verbose_name='URL'),
        ),
        migrations.AddField(
            model_name='star',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='star',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.country', verbose_name='Страна'),
        ),
        migrations.AddIndex(
            model_name='star',
            index=models.Index(fields=['-time_create'], name='main_star_time_cr_e8804b_idx'),
        ),
    ]
