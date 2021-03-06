# Generated by Django 3.2.4 on 2021-07-02 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_filemodel_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='reconciliationmodel',
            name='complete',
            field=models.BooleanField(default=False, verbose_name='Завершено'),
        ),
        migrations.AddField(
            model_name='reconciliationmodel',
            name='edited',
            field=models.BooleanField(default=False, verbose_name='На доработке'),
        ),
        migrations.AddField(
            model_name='reconciliationmodel',
            name='title',
            field=models.CharField(default='', max_length=100, verbose_name='Название'),
        ),
    ]
