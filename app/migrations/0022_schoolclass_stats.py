# Generated by Django 2.1.1 on 2018-09-15 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_remove_schoolclass_stats'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolclass',
            name='stats',
            field=models.BigIntegerField(default=0),
        ),
    ]
