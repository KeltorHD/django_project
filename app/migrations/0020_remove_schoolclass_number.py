# Generated by Django 2.0.5 on 2018-09-08 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_schoolclass_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolclass',
            name='number',
        ),
    ]
