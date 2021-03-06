# Generated by Django 3.2.5 on 2021-09-16 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210916_0904'),
        ('catalog', '0007_alter_templatemodel_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reconciliationmodel',
            name='signer',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='users.usersmodel', verbose_name='Подписывает'),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='reconciliationmodel',
            name='startDate',
            field=models.DateField(auto_now=True, verbose_name='Начало'),
        ),
    ]
