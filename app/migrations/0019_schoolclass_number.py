# Generated by Django 2.0.5 on 2018-09-01 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_schoolclass_stats'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolclass',
            name='number',
            field=models.IntegerField(default=0, help_text='Номер класса без буквы'),
            preserve_default=False,
        ),
    ]
