# Generated by Django 3.2.5 on 2021-09-13 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskcommentsmodel',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterField(
            model_name='taskmodel',
            name='startDate',
            field=models.DateField(auto_now_add=True, verbose_name='Начало'),
        ),
    ]
